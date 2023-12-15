from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class EditUserProfile(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255)])
    user_birthday = DateField('User Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('EditUserProfile')
