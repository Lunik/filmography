
from flask import Blueprint, render_template, abort, request

import tmdbsimple as tmdb

bp = Blueprint("tv", __name__, url_prefix="/")

from .forms import TVSearchForm

@bp.route("/", methods=("GET", "POST",))
def search():
  form = TVSearchForm()

  tvs = []

  if request.method == "POST":

    if not form.validate_on_submit():
      abort(400, dict(
        message="TV search failed",
        reasons=form.errors
      ))

    search = tmdb.Search()

    response = search.tv(query=form.name.data, language=request.accept_languages.best)

    tvs = response['results']

  return render_template("tv/search.html",
    search_form=form,
    tvs=tvs,
  ), 200

@bp.route("/<int:resource_id>", methods=("GET",))
def info(resource_id):
  tv = tmdb.TV(id=resource_id)

  providers = tv.watch_providers()

  print("======", providers)

  best_watch_provider=request.accept_languages.best_match(providers['results'].keys())

  return render_template("tv/info.html",
    tv_info=tv.info(language=request.accept_languages.best),
    tv_credits=tv.credits(language=request.accept_languages.best),
    tv_providers=providers['results'][best_watch_provider] if best_watch_provider else None,
  ), 200
