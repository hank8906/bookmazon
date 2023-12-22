from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    confirm_password = PasswordField('New User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    token = HiddenField()
    submit = SubmitField('RessetPassword')
