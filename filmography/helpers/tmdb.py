import logging

import tmdbsimple as tmdb
from flask import url_for

class TMDB():
  logger = logging.getLogger('gunicorn.error')
  api_key = False

  def init_app(self, flask_app):
    tmdb.API_KEY = flask_app.config["TMDB_API_KEY"]

    flask_app.tmdb = tmdb


def get_resource_image(resource_type, uri):
  if uri:
    return f"https://image.tmdb.org/t/p/w500{uri}"
  else:
    return url_for("static", filename=f"img/missing_{resource_type}.jpg")

def get_resource_url(resource_type, rid):
  return f"https://www.themoviedb.org/{resource_type}/{rid}"