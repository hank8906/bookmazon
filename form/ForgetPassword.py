from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length


class ForgetPassword(FlaskForm):
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('ForgetPassword')