from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, Regexp


class RegistryForm(FlaskForm):
    user_account = StringField('User Account', validators=[DataRequired(), Length(min=1, max=20), Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+={}\[\]|;:\'",.<>?/\\-]*$', message='只能包含英文、數字、特殊符號。')])
    user_password = PasswordField('User Password', validators=[DataRequired(), Length(min=1, max=20), Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+={}\[\]|;:\'",.<>?/\\-]*$', message='只能包含英文、數字、特殊符號。')])
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    user_gender = SelectField('User Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    user_email = StringField('User Email', validators=[DataRequired(), Email(), Length(max=255)])
    user_birthday = DateField('User Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    user_profile_picture = FileField('選擇大頭貼', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], '只能上傳jpg, png, jpeg格式的圖片!')
    ])
    submit = SubmitField('Register')
