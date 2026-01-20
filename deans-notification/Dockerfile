# Link to Repository: https://github.com/yjliew666/deans-deploy
# Source: deans-notification/Dockerfile
FROM python:3.6

ENV IN_DOCKER "1"
ENV BASEDIR /work
ENV FLASK_ROOT $BASEDIR/deans-notification
ENV PATH "$FLASK_ROOT:$BASEDIR:$PATH"

WORKDIR $BASEDIR

COPY requirements.txt $BASEDIR/
RUN pip install -r requirements.txt

COPY . $BASEDIR/
RUN sed -i -e 's/\r$//' start_server.sh && chmod +x start_server.sh

EXPOSE 8000

CMD ["./start_server.sh"]