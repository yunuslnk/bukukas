from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import get_db_connection  # Ensure you have a valid database connection function in config.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt


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

# Model Pemasukan
class Pemasukan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Fungsi untuk mendapatkan pemasukan berdasarkan ID
def get_pemasukan_by_id(id):
    return Pemasukan.query.get(id)


#=======================================================================================================
# Route for login
#=======================================================================================================
@app.route('/login', methods=['GET', 'POST'])
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
@app.route('/')
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
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    session.pop('user_id', None)  # Remove user_id from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


#=======================================================================================================
# Route for showing data (only for admins)
#=======================================================================================================
@app.route('/data')
def show_data():
    if 'role' in session and session['role'] == 'admin':  # Check if the user is an admin
        username = session['username']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')  # Show all users data
        data = cursor.fetchall()
        conn.close()
        return render_template('data.html', data=data, username=username)
    else:
        flash('You do not have permission to view this page!', 'danger')
        return redirect(url_for('home'))

@app.route('/template')
def show_template():
    if 'role' in session and session['role'] == 'admin':  # Check if the user is an admin
        username = session['username']
        #title = "Halaman Template Admin"
        return render_template('template.html', username=username)
    else:
        flash('You do not have permission to view this page!', 'danger')
        return redirect(url_for('home'))

#=======================================================================================================
# Route for adding new user (only for admins)
#=======================================================================================================

# @app.route('/transaksi')
# def transaksi():
#     if 'username' in session and session['role'] in ['admin', 'user']:
#         try:
#             username = session['username']
#             conn = get_db_connection()
#             cursor = conn.cursor()

#             # Fetch income transactions (pemasukan)
#             cursor.execute('SELECT amount, description, created_at FROM pemasukan2 WHERE user_id = ?', (session['user_id'],))
#             pemasukan_data = cursor.fetchall()

#             # Fetch expense transactions (pengeluaran)
#             cursor.execute('SELECT amount, description, created_at FROM pengeluaran WHERE user_id = ?', (session['user_id'],))
#             pengeluaran_data = cursor.fetchall()

#             conn.close()

#             return render_template('transaksi.html', pemasukan_data=pemasukan_data, pengeluaran_data=pengeluaran_data, username=username)
#         except Exception as e:
#             flash(f'Error retrieving transactions: {e}', 'danger')
#             return redirect(url_for('home'))
#     else:
#         flash('You need to login first!', 'danger')
#         return redirect(url_for('login'))

@app.route('/transaksi')
def transaksi():
    if 'username' in session and session['role'] in ['admin', 'user']:
        try:
            username = session['username']
            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch income transactions (pemasukan)
            cursor.execute('SELECT id, amount, description, created_at FROM pemasukan2 WHERE user_id = ?', (session['user_id'],))
            pemasukan_data = cursor.fetchall()

            conn.close()

            return render_template('transaksi.html', pemasukan_data=pemasukan_data, username=username)
        except Exception as e:
            flash(f'Error retrieving transactions: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))


#=======================================================================================================
#route for adding new user (only for admins)
#=======================================================================================================
@app.route('/pemasukan')
def pemasukan():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, amount, description, created_at FROM pemasukan2 WHERE user_id = ?', (session['user_id'],))
        pemasukan_data = cursor.fetchall()
        conn.close()
        return render_template('pemasukan.html', pemasukan_data=pemasukan_data)
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/add_pemasukan', methods=['POST'])
def add_pemasukan():
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pemasukan2 (amount, description, user_id, created_at)
                VALUES (?, ?, ?, GETDATE())
            """, (amount, description, session['user_id']))
            conn.commit()
            cursor.close()
            flash('Pemasukan berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksi'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/edit_pemasukan/<int:id>', methods=['GET'])
def edit_pemasukan(id):
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, amount, description FROM pemasukan2 WHERE id = ?', (id,))
        pemasukan = cursor.fetchone()
        conn.close()
        if pemasukan:
            return render_template('edit_pemasukan.html', pemasukan=pemasukan)
        else:
            flash('Pemasukan not found!', 'danger')
            return redirect(url_for('transaksi'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/update_pemasukan/<int:id>', methods=['POST'])
def update_pemasukan(id):
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pemasukan2
                SET amount = ?, description = ?
                WHERE id = ?
            """, (amount, description, id))
            conn.commit()
            cursor.close()
            flash('Pemasukan updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksi'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/delete_pemasukan/<int:id>', methods=['POST'])
def delete_pemasukan(id):
    if 'username' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pemasukan2 WHERE id = ?', (id,))
            conn.commit()
            cursor.close()
            flash('Pemasukan deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksi'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

#=======================================================================================================
#route for adding new expense (only for admins)
#=======================================================================================================
@app.route('/add_pengeluaran', methods=['POST'])
def add_pengeluaran():
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']

        # Insert data into the pengeluaran table
        try:
            conn = get_db_connection()  # Establish database connection using config.py
            if conn:
                cursor = conn.cursor()
                query = "INSERT INTO pengeluaran (amount, description, user_id) VALUES (?, ?, ?)"
                user_id = session.get('user_id')  # Fetch user_id from session
                cursor.execute(query, (amount, description, user_id))
                conn.commit()
                conn.close()

                flash('Pengeluaran berhasil ditambahkan!', 'success')
            else:
                flash('Database connection failed.', 'danger')
        except Exception as e:
            flash(f'Error saving transaction: {e}', 'danger')

        return redirect(url_for('transaksi'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

#=======================================================================================================
#=======================================================================================================
@app.route('/tabungan_mandiri')
def tabungan_mandiri():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, amount, description, created_at FROM tabungan_mandiri WHERE user_id = ?', (session['user_id'],))
        tabungan_data = cursor.fetchall()
        conn.close()
        return render_template('tabungan_mandiri.html', tabungan_data=tabungan_data)
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/add_tabungan_mandiri', methods=['POST'])
def add_tabungan_mandiri():
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tabungan_mandiri (amount, description, user_id, created_at)
                VALUES (?, ?, ?, GETDATE())
            """, (amount, description, session['user_id']))
            conn.commit()
            cursor.close()
            flash('Tabungan Mandiri berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('tabungan_mandiri'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/edit_tabungan_mandiri/<int:id>', methods=['GET'])
def edit_tabungan_mandiri(id):
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, amount, description FROM tabungan_mandiri WHERE id = ?', (id,))
        tabungan = cursor.fetchone()
        conn.close()
        if tabungan:
            return render_template('edit_tabungan_mandiri.html', tabungan=tabungan)
        else:
            flash('Tabungan Mandiri not found!', 'danger')
            return redirect(url_for('tabungan_mandiri'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/update_tabungan_mandiri/<int:id>', methods=['POST'])
def update_tabungan_mandiri(id):
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tabungan_mandiri
                SET amount = ?, description = ?
                WHERE id = ?
            """, (amount, description, id))
            conn.commit()
            cursor.close()
            flash('Tabungan Mandiri updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('tabungan_mandiri'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

@app.route('/delete_tabungan_mandiri/<int:id>', methods=['POST'])
def delete_tabungan_mandiri(id):
    if 'username' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tabungan_mandiri WHERE id = ?', (id,))
            conn.commit()
            cursor.close()
            flash('Tabungan Mandiri deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('tabungan_mandiri'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))
#=======================================================================================================
#route for register
#=======================================================================================================
if __name__ == '__main__':
    app.run(debug=True)  # Run Flask in debug mode
