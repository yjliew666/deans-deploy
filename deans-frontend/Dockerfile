FROM python:3.6

ENV IN_DOCKER "1"
ENV BASEDIR /work
ENV FLASK_ROOT $BASEDIR/deans-notification
ENV DATA_ROOT /data
ENV ENTRY_DIR $FLASK_ROOT
ENV PATH "$FLASK_ROOT:$BASEDIR:$PATH"

WORKDIR $BASEDIR
ADD requirements.txt $BASEDIR/
RUN pip install -r requirements.txt

ADD * $BASEDIR/
RUN chmod +x start_server.sh