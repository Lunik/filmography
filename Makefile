PY       ?= python3
DOCKER   ?= docker
VENV_PY  ?= venv/bin/python3
FLASK    ?= venv/bin/flask
GUNICORN ?= venv/bin/gunicorn

VENV             ?= venv
REQUIREMENTS      = requirements.txt
REQUIREMENTS_DEV  = requirements.dev.txt

APP_NAME = filmography
PACKAGE_NAME = Filmography

SERVER    ?= 127.0.0.1
PORT      ?= 8080
WORKERS   ?= 2
THREADS   ?= 2

FLASK_OPTS = --host="${SERVER}" --port="${PORT}"
ACCESSLOG_FORMAT = %(h)s %(l)s %({x-username}o)s %(t)s "%(r)s" %(s)s %(b)s "%(a)s"
GUNICORN_OPTS = --access-logfile '-' --access-logformat '${ACCESSLOG_FORMAT}' --bind="${SERVER}:${PORT}" --workers=${WORKERS} --threads=${THREADS}

APP_VERSION = $(shell git rev-parse HEAD)

install: env
	${VENV_PY} -m pip install -r "${REQUIREMENTS}"
env:
	${PY} -m venv "${VENV}"

install-docker:
	${PY} -m pip install --no-cache-dir --compile -r "${REQUIREMENTS}"

run-dev:
	DEBUG=True ${GUNICORN} ${GUNICORN_OPTS} --reload --log-level="debug" "main:app"

run: $(if $(PM_STANDALONE), database-upgrade) $(if $(PM_DEMO), demo-data)
	${GUNICORN} ${GUNICORN_OPTS} "main:app"

build-docker:
	${DOCKER} build --file="Dockerfile" --tag="${APP_NAME}:$(APP_VERSION)" .

build-docker-amd64:
	${DOCKER} build --platform Linux/amd64 --file="Dockerfile" --tag="${APP_NAME}:$(APP_VERSION)" .
