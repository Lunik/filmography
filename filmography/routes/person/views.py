
from flask import Blueprint, render_template, abort, request

import tmdbsimple as tmdb

bp = Blueprint("person", __name__, url_prefix="/")

from .forms import PersonSearchForm

@bp.route("/", methods=("GET", "POST",))
def search():
  form = PersonSearchForm()

  persons = []

  if request.method == "POST":

    if not form.validate_on_submit():
      abort(400, dict(
        message="Person search failed",
        reasons=form.errors
      ))

    search = tmdb.Search()

    response = search.person(query=form.name.data, language=request.accept_languages.best)

    persons = response['results']

  return render_template("person/search.html",
    search_form=form,
    persons=persons,
  ), 200

@bp.route("/<int:resource_id>", methods=("GET",))
def info(resource_id):
  person = tmdb.People(id=resource_id)

  return render_template("person/info.html",
    person_info=person.info(language=request.accept_languages.best),
    person_movies=person.movie_credits(language=request.accept_languages.best),
    person_tvs=person.tv_credits(language=request.accept_languages.best),
  ), 200
