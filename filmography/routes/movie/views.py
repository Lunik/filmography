
from flask import Blueprint, render_template, abort, request

import tmdbsimple as tmdb

bp = Blueprint("movie", __name__, url_prefix="/")

from .forms import MovieSearchForm

@bp.route("/", methods=("GET", "POST",))
def search():
  form = MovieSearchForm()

  movies = []

  if request.method == "POST":

    if not form.validate_on_submit():
      abort(400, dict(
        message="Movie search failed",
        reasons=form.errors
      ))

    search = tmdb.Search()

    response = search.movie(query=form.name.data, language=request.accept_languages.best)

    movies = response['results']

  return render_template("movie/search.html",
    search_form=form,
    movies=movies,
  ), 200

@bp.route("/<int:resource_id>", methods=("GET",))
def info(resource_id):
  movie = tmdb.Movies(id=resource_id)

  providers = movie.watch_providers()

  best_watch_provider=request.accept_languages.best_match(providers['results'].keys())

  return render_template("movie/info.html",
    movie_info=movie.info(language=request.accept_languages.best),
    movie_credits=movie.credits(language=request.accept_languages.best),
    movie_providers=providers['results'][best_watch_provider] if best_watch_provider else None,
  ), 200
