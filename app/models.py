from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from app import s
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(login_id):
    return Login.query.get(int(login_id))

class Login(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(15), nullable=False)
    nama = db.Column(db.String(50), nullable=False) 
    fakultas = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    telpon = db.Column(db.String(15), nullable=False)
    tahun = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    

class Dosen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nidn = db.Column(db.String(15), nullable=False)
    nama = db.Column(db.String(50), nullable=False) 
    fakultas = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    telpon = db.Column(db.String(15), nullable=False)
    tahun = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    kuota = db.Column(db.Integer, nullable=False)
    

class Pedoman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Pedoman('{self.nama}')"


class Pengajuan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    perusahaan = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    balasan = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    id_dospem = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    isi = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.judul}', '{self.tanggal}')"

    @hybrid_property
    def danger(self):
        return s.dumps(self.id)


class Bimbingan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kreatifitas = db.Column(db.Text, nullable=False)
    metode = db.Column(db.Text, nullable=False)
    file_pkl = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    komen_dosen = db.Column(db.Text, nullable=False)
    komen_mhs = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
