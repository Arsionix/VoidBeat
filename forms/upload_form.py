from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class UploadTrackForm(FlaskForm):
    title = StringField('Название трека', validators=[DataRequired()])
    artist = StringField('Исполнитель', validators=[DataRequired()])
    mode = SelectField('Режим', choices=[
        ('flow', 'Flow'),
        ('deep', 'Deep'),
        ('reset', 'Reset')
    ], validators=[DataRequired()])
    audio_file = FileField('Аудиофайл (MP3)', validators=[
        FileAllowed(['mp3'], 'Только MP3 файлы!')
    ])
    submit = SubmitField('Загрузить')
