from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Login, Mahasiswa, Dosen, Pedoman, Pengajuan, Post, Bimbingan

class RegistrasiForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Daftar')

	def validate_username(self, username):
		user = Login.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username Sudah Ada Silahkan Pilih Yang Lain')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Masuk')

class DosenForm(FlaskForm):
	nidn = StringField('nidn', validators=[DataRequired()])
	nama = StringField('nama', validators=[DataRequired()])
	fakultas = StringField('fakultas', validators=[DataRequired()])
	alamat = StringField('alamat', validators=[DataRequired()])
	telpon = StringField('telepon', validators=[DataRequired()])
	tahun = StringField('tahun', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	kuota = StringField('kuota', validators=[DataRequired()])
	submit = SubmitField('Tambah')
	
class PostForm(FlaskForm):
	judul = StringField('Judul', validators=[DataRequired()])
	isi = TextAreaField('Isi', validators=[DataRequired()])
	submit = SubmitField('post')



