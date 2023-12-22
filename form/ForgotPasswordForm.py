from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ForgotPasswordForm(FlaskForm):
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField('ForgotPassword')
