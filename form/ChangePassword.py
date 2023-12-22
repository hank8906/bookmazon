from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('User Current Password', validators=[DataRequired(), Length(min=1, max=20)])
    new_password = PasswordField('User New Password', validators=[DataRequired(), Length(min=1, max=20)])

    submit = SubmitField('ChangePassword')
