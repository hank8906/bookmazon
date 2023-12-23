from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class EditUserProfile(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255), Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+={}\[\]|;:\'",.<>?/\\-]*$', message='只能包含英文、數字、特殊符號。')])
    user_birthday = DateField('User Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('EditUserProfile')
