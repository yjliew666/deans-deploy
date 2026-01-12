FROM python:3.8

ENV IN_DOCKER "1"
ENV BASEDIR /work
ENV FLASK_ROOT $BASEDIR
ENV DATA_ROOT /data
ENV ENTRY_DIR $FLASK_ROOT
ENV PATH "$FLASK_ROOT:$BASEDIR:$PATH"

WORKDIR $BASEDIR

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl dos2unix && rm -rf /var/lib/apt/lists/*

COPY requirements.txt $BASEDIR/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all files
COPY . $BASEDIR/

# Fix line endings and make executable
RUN dos2unix start_server.sh && chmod +x start_server.sh

CMD ["/bin/bash", "./start_server.sh"]

