from flask import Flask, render_template, request, redirect, url_for, flash, session    
from config import get_db_connection  # get_db_connection: Koneksi ke database (diambil dari config.py).
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy: ORM untuk interaksi database.
import bcrypt # bcrypt: Modul untuk mengenkripsi kata sandi.
from reportlab.lib.pagesizes import letter # letter: Ukuran halaman standar.
from reportlab.pdfgen import canvas # canvas: Modul untuk membuat PDF.
from io import BytesIO # BytesIO: Modul untuk bekerja dengan data biner.
from flask import Response, send_file # Response: Merespons permintaan HTTP. send_file: Mengirim file ke pengguna.
from datetime import datetime, timedelta # timedelta: Durasi waktu.
import os # os: Modul untuk berinteraksi dengan sistem operasi.
from werkzeug.utils import secure_filename # secure_filename: Mengamankan nama file.
from template import show_template  # Impor fungsi dari file template.py
#from aset import aset, allowed_file, add_aset, update_aset, delete_aset, edit_aset  # Impor fungsi dari file aset.py

app = Flask(__name__)
app.secret_key = 'secret123'  # Encryption key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bukukas.db'  # Ganti dengan database Anda
db = SQLAlchemy(app)


#=======================================================================================================
# Simulasi database user
#=======================================================================================================
users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}

#=======================================================================================================
# Route for login
#=======================================================================================================
#app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database and verify the user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()  # Fetch user from the database
        conn.close()

        # If the user exists and the password matches
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Adjust column index if necessary
            session['username'] = username
            session['user_id'] = user[0]
            session['role'] = user[4]  # Store role in session (e.g., 'admin' or 'user')
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')

    return render_template('login.html')


#=======================================================================================================
# Route for the main page (home)
#=======================================================================================================
#@app.route('/')
def home():
    if 'username' in session and 'role' in session:
        username = session['username']
        role = session['role']
        return render_template('home.html', username=username, role=role)
    else:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

#=======================================================================================================
# Route for logging out
#=======================================================================================================
#@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)  # Remove user_id from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



