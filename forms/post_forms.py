from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    media = FileField("Upload Image/Audio/Video", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mp3'], 'Media files only!')
    ])
    is_published = BooleanField("Publish now?")
    submit = SubmitField("Submit")
