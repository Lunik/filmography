FROM python:3-alpine

# Dockerfile arguments
ARG APP_DIR=/app
ARG USER=filmography
ARG PORT=8080


# Define base configuration
ENV PYTHONPATH=$APP_DIR
ENV GUNICORN=/usr/local/bin/gunicorn
ENV FLASK=/usr/local/bin/flask
ENV SERVER=0.0.0.0
ENV PORT=$PORT


# Change base directory
WORKDIR $APP_DIR


# Create application user & work directory
RUN adduser \
    -u 1000 \
    -D -H \
    -h $APP_DIR \
    $USER


# Upgrade base image
RUN apk upgrade \
  --update --no-cache \
  && apk add \
  --update --no-cache \
  make ca-certificates


# Install required libraries/packages
COPY Makefile ./
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
  apk add --update --no-cache --virtual .build build-base \
    libxml2-dev libxslt-dev \
  && make install-docker \
  && apk del .build

RUN --mount=type=bind,source=patches,target=patches \
  apk add --update --no-cache --virtual .build patch \
  && patch -u /usr/local/lib/python3.11/site-packages/tmdbsimple/tv.py patches/tv_watch_providers.patch \
  && apk del .build


# Copy application sources
COPY filmography filmography
COPY main.py .flaskenv ./


# Compile app Python files
RUN python -m compileall filmography main.py


# Change user for runtime
USER $USER

# Declare application listen port
EXPOSE $PORT

# Declare application command start
CMD ["make", "run"]