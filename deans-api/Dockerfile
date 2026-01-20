# Link to Repository: https://github.com/yjliew666/deans-deploy
# Source: deans-api/Dockerfile
FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV IN_DOCKER "1"
ENV BASEDIR /work
ENV DJANGO_ROOT $BASEDIR/deans_api
ENV PATH "$DJANGO_ROOT:$BASEDIR:$PATH"

WORKDIR $BASEDIR

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt $BASEDIR/
RUN pip install -r requirements.txt

COPY start_django.sh $BASEDIR/
RUN sed -i -e 's/\r$//' start_django.sh && chmod +x start_django.sh

COPY . $BASEDIR/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]