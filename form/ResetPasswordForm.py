from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New User Password', validators=[DataRequired(), Length(min=1, max=20)])
    confirm_password = PasswordField('New User Password', validators=[DataRequired(), Length(min=1, max=20)])
    token = HiddenField()
    submit = SubmitField('RessetPassword')
