from flask import Flask, render_template, url_for, redirect, flash, redirect, session, request, send_file
from app import app, db, s
from app.models import Login, Mahasiswa, Dosen, Pedoman, Pengajuan, Post, Bimbingan
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import RegistrasiForm, LoginForm, DosenForm, PostForm
from io import BytesIO

@app.route('/')
@app.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)

@app.route('/dosen')
def dosen():
	dosen = Dosen.query.all()
	return render_template('dosen.html',title='Dosen', dosen=dosen)


@app.route('/edit_dosen', methods=['GET', 'POST'])
def edit_dosen():
	form = DosenForm()
	dosen = Dosen.query.all()
	if form.validate_on_submit():
		dosen = Dosen(nidn= form.nidn.data, nama= form.nama.data, fakultas = form.fakultas.data, 
			alamat= form.alamat.data, telpon= form.telpon.data, tahun= form.tahun.data, 
			email= form.email.data, kuota= form.kuota.data )
		db.session.add(dosen)
		db.session.commit()
		flash(f' {form.nama.data} Berhasil Di Buat ', 'success')
		return redirect(url_for('edit_dosen'))
	return render_template('edit_dosen.html',title='Dosen', form=form, dosen=dosen)

@app.route('/tambah_dosen', methods=['GET', 'POST'])
@login_required
def tambah_dosen():
	form = DosenForm()
	if form.validate_on_submit():
		dosen = Dosen(nidn= form.nidn.data, nama= form.nama.data, fakultas = form.fakultas.data, 
			alamat= form.alamat.data, telpon= form.telpon.data, tahun= form.tahun.data, 
			email= form.email.data, kuota= form.kuota.data )
		db.session.add(dosen)
		db.session.commit()
		flash(f' {form.nama.data} Berhasil Di Buat ', 'success')
		return redirect(url_for('edit_dosen'))
	return render_template('tambah_dosen.html', form=form)

@app.route('/pedoman', methods=['GET', 'POST'])
def pedoman():
	pedoman = Pedoman.query.all()
	if request.method == 'POST':
		file = request.files['savefile']
		newfile = Pedoman(nama=file.filename, data=file.read())
		db.session.add(newfile)
		db.session.commit()
		flash(f' {file.filename} Berhasil Di Upload ', 'success')
		return redirect(url_for('pedoman'))
	return render_template('pedoman.html',title='Pedoman', pedoman=pedoman)

@app.route("/pedoman_download/<pedoman_id>")
def pedoman_download(pedoman_id):
	pedoman = Pedoman.query.get_or_404(pedoman_id)
	return send_file(BytesIO(pedoman.data), attachment_filename=f'{pedoman.nama}', as_attachment=True)

@app.route('/download')
def download():
	file = Pedoman.query.filter_by(id=1).first()
	return send_file(BytesIO(file.data), attachment_filename=f'{file.nama}', as_attachment=True)
	# return render_template('pedoman.html',title='Pedoman', file=file )

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated :
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Login.query.filter_by(username=form.username.data).first()
		if user and form.password.data :
			login_user(user)
			flash('Login Berhasil', 'success')
			return redirect(url_for('home'))
		else :
			flash('Login gagal', 'danger')
	return render_template('login.html', form=form)

@app.route('/registrasi', methods=['GET', 'POST'])
def registrasi():
	if current_user.is_authenticated :
		return redirect(url_for('home')) 
	form = RegistrasiForm()
	if form.validate_on_submit():
		user = Login(username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Registrasi {form.username.data} Berhasi', 'success')
		return redirect(url_for('login'))

	return render_template('registrasi.html', form=form)



@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home')) 


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(judul = form.judul.data, isi=form.isi.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f'{form.judul.data} Berhasil di upload', 'success')
		return redirect(url_for('home'))
	return render_template('pengumuman.html', title='isi konten', form=form)

@app.route("/post/<post_id>")
def post(post_id):
	post_id = s.loads(post_id)
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.judul, post=post)