from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, length, equal_to


class LoginForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired(), length(min=8, max=64)])
    submit = SubmitField("შესვლა")


