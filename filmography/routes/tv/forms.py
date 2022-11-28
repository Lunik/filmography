from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import DataRequired

class TVSearchForm(FlaskForm):
  name = StringField(
    name='name',
    label="Name",
    validators=[DataRequired()],
  )