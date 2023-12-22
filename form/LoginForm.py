from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    user_account = StringField('User Account', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9'
                                                                                                         ']*$',
                                                                                                         message='只能包含英文和數字。')])
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^['
                                                                                                             'a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    submit = SubmitField('Login')
