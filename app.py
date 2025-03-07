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
from aset import aset, allowed_file, add_aset, update_aset, delete_aset, edit_aset, calculate_total_pages  # Impor fungsi dari file aset.py
from user import login, home, logout  # Impor fungsi dari file user.py




 # from aset import allowed_file
# from aset import add_aset
# from aset import update_aset
# from aset import delete_aset
# from aset import edit_aset
 

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#allowed_file(filename) memeriksa apakah nama file yang diberikan memiliki ekstensi yang diizinkan.


app = Flask(__name__)
app.secret_key = 'secret123'  # Encryption key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bukukas.db'  # Ganti dengan database Anda
db = SQLAlchemy(app)
# Route 
app.add_url_rule('/template', 'show_template', show_template)
app.add_url_rule('/aset', 'aset', aset, methods=['GET'])
app.add_url_rule('/add_aset', 'add_aset', add_aset, methods=['POST'])
app.add_url_rule('/edit_aset/<int:id>', 'edit_aset', edit_aset, methods=['GET', 'POST'])
app.add_url_rule('/update_aset/<int:id>', 'update_aset', update_aset, methods=['POST'])
app.add_url_rule('/delete_aset/<int:id>', 'delete_aset', delete_aset, methods=['POST'])

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/', 'home', home)
app.add_url_rule('/logout', 'logout', logout)




# Set the folder for uploaded files
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Connect to the database and verify the user
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
#         user = cursor.fetchone()  # Fetch user from the database
#         conn.close()

#         # If the user exists and the password matches
#         if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Adjust column index if necessary
#             session['username'] = username
#             session['user_id'] = user[0]
#             session['role'] = user[4]  # Store role in session (e.g., 'admin' or 'user')
#             flash('Login successful!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid credentials!', 'danger')

#     return render_template('login.html')

#=======================================================================================================
# Route for the main page (home)
#=======================================================================================================
# @app.route('/')
# def home():
#     if 'username' in session and 'role' in session:
#         username = session['username']
#         role = session['role']
#         return render_template('home.html', username=username, role=role)
#     else:
#         flash('Please log in first', 'warning')
#         return redirect(url_for('login'))

#=======================================================================================================
# Route for logging out
#=======================================================================================================
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     session.pop('role', None)
#     session.pop('user_id', None)  # Remove user_id from session
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))


#=======================================================================================================
# Route for showing data (only for admins)
#=======================================================================================================
# @app.route('/data')
# def show_data():
#     if 'role' in session and session['role'] == 'admin':  # Check if the user is an admin
#         username = session['username']
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM users')  # Show all users data
#         data = cursor.fetchall()
#         conn.close()
#         return render_template('data.html', data=data, username=username)
#     else:
#         flash('You do not have permission to view this page!', 'danger')
#         return redirect(url_for('home'))


@app.route('/tables')
def show_tables():
    if 'role' in session and session['role'] == 'admin':  # Check if the user is an admin
        username = session['username']
        #title = "Halaman Template Admin"
        return render_template('tables.html', username=username)
    else:
        flash('You do not have permission to view this page!', 'danger')
        return redirect(url_for('home'))

# Transaksi Pemasukan
@app.route('/transaksipemasukan', methods=['GET'])
def transaksipemasukan():
    if 'username' in session and session['role'] in ['admin', 'user']:
        try:
            username = session['username']
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get today's date
            today = datetime.today()

            # Default for current month (first and last day)
            first_day_of_month = today.replace(day=1)
            last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            # Get start and end dates from query parameters or use defaults
            start_date = request.args.get('start_date', first_day_of_month.strftime('%Y-%m-%d'))
            end_date = request.args.get('end_date', last_day_of_month.strftime('%Y-%m-%d'))
            
        

            # Fetch pemasukan (income) data
            query_pemasukan = '''SELECT id, amount, description, created_at, bukti_transfer 
                                 FROM pemasukan2 
                                 WHERE user_id = ?'''
            params_pemasukan = [session['user_id']]

            if start_date and end_date:
                query_pemasukan += ' AND created_at BETWEEN ? AND ?'
                params_pemasukan.extend([start_date, end_date])

            cursor.execute(query_pemasukan, params_pemasukan)
            pemasukan_data = cursor.fetchall()

            # Calculate total pemasukan
            total_pemasukan = sum(pemasukan[1] for pemasukan in pemasukan_data)

            # Format pemasukan data
            formatted_pemasukan_data = []
            for pemasukan in pemasukan_data:
                formatted_date = pemasukan[3].strftime('%d-%m-%Y')
                formatted_amount = f"Rp. {int(pemasukan[1]):,}".replace(',', '.')
                formatted_pemasukan_data.append((pemasukan[0], formatted_amount, pemasukan[2], formatted_date, pemasukan[4]))

            
            # Format total amounts
            formatted_total_pemasukan = f"Rp. {int(total_pemasukan):,}".replace(',', '.')

            conn.close()

            # Render both pemasukan and pengeluaran data in the template
            return render_template('transaksi_pemasukan.html', 
                                   pemasukan_data=formatted_pemasukan_data, 
                                   total_pemasukan=formatted_total_pemasukan,
                                   start_date=start_date, 
                                   end_date=end_date, 
                                   username=username)
        except Exception as e:
            flash(f'Error retrieving transactions: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))




# Transaksi Pengeluaran
@app.route('/transaksipengeluaran', methods=['GET'])
def transaksipengeluaran():
    if 'username' in session and session['role'] in ['admin', 'user']:
        try:
            username = session['username']
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get today's date
            today = datetime.today()

            # Default for current month (first and last day)
            first_day_of_month = today.replace(day=1)
            last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            # Get start and end dates from query parameters or use defaults
            start_date = request.args.get('start_date', first_day_of_month.strftime('%Y-%m-%d'))
            end_date = request.args.get('end_date', last_day_of_month.strftime('%Y-%m-%d'))
            
            # Fetch pengeluaran (expenses) data
            query_pengeluaran = '''SELECT id, amount, description, created_at, bukti_transfer 
                                   FROM pengeluaran2 
                                   WHERE user_id = ?'''
            params_pengeluaran = [session['user_id']]

            if start_date and end_date:
                query_pengeluaran += ' AND created_at BETWEEN ? AND ?'
                params_pengeluaran.extend([start_date, end_date])

            cursor.execute(query_pengeluaran, params_pengeluaran)
            pengeluaran_data = cursor.fetchall()

            # Calculate total pengeluaran
            total_pengeluaran = sum(pengeluaran[1] for pengeluaran in pengeluaran_data)

            # Format pengeluaran data
            formatted_pengeluaran_data = []
            for pengeluaran in pengeluaran_data:
                formatted_date = pengeluaran[3].strftime('%d-%m-%Y')
                formatted_amount = f"Rp. {int(pengeluaran[1]):,}".replace(',', '.')
                formatted_pengeluaran_data.append((pengeluaran[0], formatted_amount, pengeluaran[2], formatted_date, pengeluaran[4]))

            # Format total amounts
            formatted_total_pengeluaran = f"Rp. {int(total_pengeluaran):,}".replace(',', '.')

            conn.close()

            # Render both pemasukan and pengeluaran data in the template
            return render_template('transaksi_pengeluaran.html', 
                                   pengeluaran_data=formatted_pengeluaran_data, 
                                   total_pengeluaran=formatted_total_pengeluaran,
                                   start_date=start_date, 
                                   end_date=end_date, 
                                   username=username)
        except Exception as e:
            flash(f'Error retrieving transactions: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))


#total pengeluaran

#=======================================================================================================
#route for adding new user (only for admins)
#=======================================================================================================


#bisa upload gambar


@app.route('/add_pemasukan', methods=['POST'])
def add_pemasukan():
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        created_at = request.form['created_at']

        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(created_at, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('transaksipemasukan' ))

        # Validate and round the amount
        try:
            amount = round(float(amount), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('transaksipemasukan' ))

        # Handle image upload (if provided)
        file = request.files.get('bukti_transfer')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif file:
            flash('Invalid file type! Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')
            return redirect(url_for('transaksipemasukan' ))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert the income (pemasukan) data with image filename (if uploaded)
            cursor.execute("""
                INSERT INTO pemasukan2 (amount, description, user_id, created_at, bukti_transfer)
                VALUES (?, ?, ?, ?, ?)
            """, (amount, description, session['user_id'], created_at, filename))
            
            conn.commit()
            cursor.close()
            flash('Pemasukan berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('transaksipemasukan', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))



#pengeluaran
@app.route('/add_pengeluaran', methods=['POST'])
def add_pengeluaran():
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        created_at = request.form['created_at']

        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(created_at, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('transaksipengeluaran'))

        # Validate and round the amount
        try:
            amount = round(float(amount), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('transaksipengeluaran'))

        # Handle image upload (if provided)
        file = request.files.get('bukti_transfer')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif file:
            flash('Invalid file type! Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')
            return redirect(url_for('transaksipengeluaran'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insert the income (pengeluaran) data with image filename (if uploaded)
            cursor.execute("""
                INSERT INTO pengeluaran2 (amount, description, user_id, created_at, bukti_transfer)
                VALUES (?, ?, ?, ?, ?)
            """, (amount, description, session['user_id'], created_at, filename))
            
            conn.commit()
            cursor.close()
            flash('pengeluaran berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('transaksipengeluaran', show_collapse=True))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))





#edit upload gambar
@app.route('/edit_pemasukan/<int:id>', methods=['GET', 'POST'])
def edit_pemasukan(id):
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Ensure 'created_at' exists in the request form
            if 'created_at' not in request.form:
                flash('Tanggal pemasukan tidak tersedia!', 'danger')
                return redirect(url_for('edit_pemasukan', id=id))

            # Fetch the form data
            amount = request.form['amount']
            description = request.form['description']
            created_at = request.form['created_at']

            # Handle file upload for 'bukti_transfer'
            file = request.files.get('bukti_transfer')
            bukti_transfer_filename = None

            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                # Save the file to the uploads folder
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                bukti_transfer_filename = filename  # Store the filename to update in DB

            # Update the record, including the image if uploaded
            if bukti_transfer_filename:
                cursor.execute('UPDATE pemasukan2 SET amount = ?, description = ?, created_at = ?, bukti_transfer = ? WHERE id = ?',
                               (amount, description, created_at, bukti_transfer_filename, id))
            else:
                cursor.execute('UPDATE pemasukan2 SET amount = ?, description = ?, created_at = ? WHERE id = ?',
                               (amount, description, created_at, id))

            conn.commit()
            conn.close()

            flash('Pemasukan updated successfully!', 'success')
            return redirect(url_for('transaksipemasukan', show_collapse=True))
        else:
            # If it's a GET request, display the existing data
            cursor.execute('SELECT id, amount, description, created_at, bukti_transfer FROM pemasukan2 WHERE id = ?', (id,))
            pemasukan = cursor.fetchone()
            conn.close()

            if pemasukan:
                # Format the amount and date
                formatted_pemasukan = (pemasukan[0], int(pemasukan[1]), pemasukan[2], pemasukan[3], pemasukan[4])
                return render_template('edit_pemasukan.html', pemasukan=formatted_pemasukan)
            else:
                flash('Pemasukan not found!', 'danger')
                return redirect(url_for('transaksipemasukan', show_collapse=True))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))


#edit pengeluaran
@app.route('/edit_pengeluaran/<int:id>', methods=['GET', 'POST'])
def edit_pengeluaran(id):
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Ensure 'created_at' exists in the request form
            if 'created_at' not in request.form:
                flash('Tanggal pengeluaran tidak tersedia!', 'danger')
                return redirect(url_for('edit_pengeluaran', id=id))

            # Fetch the form data
            amount = request.form['amount']
            description = request.form['description']
            created_at = request.form['created_at']

            # Handle file upload for 'bukti_transfer'
            file = request.files.get('bukti_transfer')
            bukti_transfer_filename = None

            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                # Save the file to the uploads folder
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                bukti_transfer_filename = filename  # Store the filename to update in DB

            # Update the record, including the image if uploaded
            if bukti_transfer_filename:
                cursor.execute('UPDATE pengeluaran2 SET amount = ?, description = ?, created_at = ?, bukti_transfer = ? WHERE id = ?',
                               (amount, description, created_at, bukti_transfer_filename, id))
            else:
                cursor.execute('UPDATE pengeluaran2 SET amount = ?, description = ?, created_at = ? WHERE id = ?',
                               (amount, description, created_at, id))

            conn.commit()
            conn.close()

            flash('pengeluaran updated successfully!', 'success')
            return redirect(url_for('transaksipengeluaran', show_collapse=True ))
        else:
            # If it's a GET request, display the existing data
            cursor.execute('SELECT id, amount, description, created_at, bukti_transfer FROM pengeluaran2 WHERE id = ?', (id,))
            pengeluaran = cursor.fetchone()
            conn.close()

            if pengeluaran:
                # Format the amount and date
                formatted_pengeluaran = (pengeluaran[0], int(pengeluaran[1]), pengeluaran[2], pengeluaran[3], pengeluaran[4])
                return render_template('edit_pengeluaran.html', pengeluaran=formatted_pengeluaran)
            else:
                flash('pengeluaran not found!', 'danger')
                return redirect(url_for('transaksipengeluaran', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))
    


#edit tanggal
@app.route('/update_pemasukan/<int:id>', methods=['POST'])
def update_pemasukan(id):
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        created_at = request.form['created_at']  # Get the date from the form

        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(created_at, '%Y-%m-%d')  # Check if the date is valid
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('transaksipemasukan'))

        # Round the amount to 2 decimal places
        try:
            amount = round(float(amount), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('transaksipemasukan'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pemasukan2
                SET amount = ?, description = ?, created_at = ?
                WHERE id = ?
            """, (amount, description, created_at, id))
            conn.commit()
            cursor.close()
            flash('Pemasukan updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksipemasukan', show_collapse=True))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))




#edit tanggal
@app.route('/update_pengeluaran/<int:id>', methods=['POST'])
def update_pengeluaran(id):
    if 'username' in session:
        amount = request.form['amount']
        description = request.form['description']
        created_at = request.form['created_at']  # Get the date from the form

        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(created_at, '%Y-%m-%d')  # Check if the date is valid
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('transaksipengeluaran'))

        # Round the amount to 2 decimal places
        try:
            amount = round(float(amount), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('transaksipengeluaran'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pengeluaran2
                SET amount = ?, description = ?, created_at = ?
                WHERE id = ?
            """, (amount, description, created_at, id))
            conn.commit()
            cursor.close()
            flash('pengeluaran updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksipengeluaran', show_collapse=True ))
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
        return redirect(url_for('transaksipemasukan', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))



@app.route('/delete_pengeluaran/<int:id>', methods=['POST'])
def delete_pengeluaran(id):
    if 'username' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM pengeluaran2 WHERE id = ?', (id,))
            conn.commit()
            cursor.close()
            flash('pengeluaran deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('transaksipengeluaran', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

#=======================================================================================================
#route for register
#=======================================================================================================
if __name__ == '__main__':
    app.run(debug=True)  # Run Flask in debug mode
