from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp


class RegistryForm(FlaskForm):
    user_account = StringField('User Account', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp('^[a-zA-Z0-9]*$', message='只能包含英文和數字。')])
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    user_gender = SelectField('User Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255)])
    user_birthday = DateField('User Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Register')
