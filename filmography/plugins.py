
from flask_wtf.csrf import CSRFProtect
from .helpers.tmdb import TMDB

csrf = CSRFProtect()
tmdb = TMDB()