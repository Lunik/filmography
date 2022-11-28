import os
import logging
from datetime import timedelta

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask

from .helpers.config import boolean_param
from .plugins import csrf, tmdb

def create_app():
  app = Flask(
    __name__,
    instance_relative_config=True,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates'
  )

  app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=os.environ.get(
      "PM_SECRET_KEY",
      "changeit"
    ),
    APP_NAME="Filmography",
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_CHECK_DEFAULT=False,
    DEBUG=boolean_param(os.environ.get("DEBUG", 'False')),
    TMDB_API_KEY=os.environ.get("TMDB_API_KEY", None),
  )

  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=int(os.environ.get("PM_PROXY_CHAIN_COUNT", 1)), x_proto=1)

  csrf.init_app(app)
  tmdb.init_app(app)

  # apply Gunicorn logger config
  gunicorn_logger = logging.getLogger('gunicorn.error')
  gunicorn_logger.setLevel(gunicorn_logger.level)
  app.logger.handlers = gunicorn_logger.handlers

  from .routes import root, person, movie, tv
  # apply the blueprints to the app
  app.register_blueprint(root.view, url_prefix="/")
  app.register_blueprint(person.view, url_prefix="/person")
  app.register_blueprint(movie.view, url_prefix="/movie")
  app.register_blueprint(tv.view, url_prefix="/tv")

  from .helpers.tmdb import get_resource_image, get_resource_url
  # Add Jinja2 filters
  app.jinja_env.globals['get_resource_image'] = get_resource_image
  app.jinja_env.globals['get_resource_url'] = get_resource_url

  return app
