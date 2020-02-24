from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, InputRequired, Email
from wtforms import StringField, TextField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
images = ['png', 'jpg', 'jpeg', 'gif']
class UploadForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])