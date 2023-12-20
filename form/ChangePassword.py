from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('User Current Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    new_password = PasswordField('User New Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])

    submit = SubmitField('ChangePassword')
