from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    user_account = StringField('User Account', validators=[DataRequired(), Length(min=1, max=20)])
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Login')
