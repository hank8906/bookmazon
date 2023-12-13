from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length


class ForgetPassword(FlaskForm):
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('ForgetPassword')