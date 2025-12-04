# providers/report_pdf.py
from typing import Dict, Any
from .base import NotificationProvider
import report_generation


class ReportPDFProvider(NotificationProvider):
    """
    Strategy wrapper around report_generation.py.

    Expected payload keys:
    - 'report_count': integer index used to select the JSON input and output file path.
      For example:
        json_summary/json{report_count}.json -> reports/report{report_count}.pdf

    This provider only generates the PDF file; it does not send email.
    """

    def send(self, payload: Dict[str, Any]) -> bool:
        report_count = payload.get("report_count")

        if report_count is None:
            print("ReportPDFProvider: missing 'report_count' in payload")
            return False

        try:
            # Ensure template is compiled (optional; you can call compiling() once or assume done)
            report_generation.compiling()
            report_generation.json_to_pdf(report_count)
            return True
        except Exception as e:
            print("ReportPDFProvider error:", e)
            return False
