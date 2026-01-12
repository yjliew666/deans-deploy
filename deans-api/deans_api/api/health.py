from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import time
import logging

logger = logging.getLogger("django")

def health_check(request):
    """
    Health check endpoint for monitoring and orchestration.
    Returns 200 if all critical services are up, 503 if any are down.
    """
    checks = {}
    overall_status = "healthy"
    status_code = 200
    
    # Check 1: Database connectivity
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        latency_ms = round((time.time() - start) * 1000, 2)
        checks["database"] = {
            "status": "up",
            "latency_ms": latency_ms,
            "type": connection.settings_dict['ENGINE']
        }
        logger.debug(f"Database health check passed ({latency_ms}ms)")
    except Exception as e:
        checks["database"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "unhealthy"
        status_code = 503
        logger.error(f"Database health check failed: {e}")
    
    # Check 2: Redis connectivity (for Channels)
    try:
        start = time.time()
        cache.set('health_check', 'ok', timeout=10)
        result = cache.get('health_check')
        latency_ms = round((time.time() - start) * 1000, 2)
        
        if result == 'ok':
            checks["redis"] = {
                "status": "up",
                "latency_ms": latency_ms
            }
            logger.debug(f"Redis health check passed ({latency_ms}ms)")
        else:
            raise Exception("Cache value mismatch")
    except Exception as e:
        checks["redis"] = {
            "status": "down",
            "error": str(e)
        }
        overall_status = "unhealthy"
        status_code = 503
        logger.error(f"Redis health check failed: {e}")
    
    # Check 3: Channels WebSocket layer
    try:
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        if channel_layer:
            checks["channels"] = {"status": "up"}
            logger.debug("Channels layer health check passed")
        else:
            raise Exception("Channel layer not configured")
    except Exception as e:
        checks["channels"] = {
            "status": "down",
            "error": str(e)
        }
        # WebSocket is non-critical, don't mark overall as unhealthy
        logger.warning(f"Channels health check failed: {e}")
    
    response_data = {
        "status": overall_status,
        "timestamp": timezone.now().isoformat(),
        "checks": checks,
        "version": "1.0.0"
    }
    
    return JsonResponse(response_data, status=status_code)


def readiness_check(request):
    """
    Readiness check - lighter than health check.
    Returns 200 if app is ready to accept traffic.
    """
    try:
        # Quick DB check only
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready"}, status=200)
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JsonResponse({"status": "not_ready", "error": str(e)}, status=503)