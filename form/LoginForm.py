from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    user_account = StringField('User Account', validators=[DataRequired(), Length(min=1, max=20), Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+={}\[\]|;:\'",.<>?/\\-]*$', message='只能包含英文、數字、特殊符號。')])
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+={}\[\]|;:\'",.<>?/\\-]*$', message='只能包含英文、數字、特殊符號。')])
    submit = SubmitField('Login')
