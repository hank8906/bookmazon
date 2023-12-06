from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length


class ChangePassword(FlaskForm):
    current_password = PasswordField('User Current Password', validators=[DataRequired(), Length(min=1, max=20)])
    new_password = PasswordField('User New Password', validators=[DataRequired(), Length(min=1, max=20)])

    submit = SubmitField('ChangePassword')
