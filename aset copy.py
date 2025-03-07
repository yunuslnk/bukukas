
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Set the folder for uploaded files
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Transaksi Aset
#@app.route('/aset', methods=['GET'])
def aset():
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
            
        

            # Fetch Aset data
            query_aset = '''SELECT id, asset_name, description, owner, category, price, purchase_date, asset_image 
                                 FROM tbl_aset 
                                 WHERE user_id = ?'''
            params_aset = [session['user_id']]

            if start_date and end_date:
                query_aset += ' AND purchase_date BETWEEN ? AND ?'
                params_aset.extend([start_date, end_date])

            cursor.execute(query_aset, params_aset)
            aset_data = cursor.fetchall()

            # Calculate total aset
            total_aset = sum(aset[5] for aset in aset_data)

            # Format aset data

            formatted_aset_data = []
            for aset in aset_data:
                formatted_date = aset[6].strftime('%d-%m-%Y')
                formatted_amount = f"Rp. {int(aset[5]):,}".replace(',', '.')
                formatted_aset_data.append((aset[0], aset[1], aset[2], aset[3], aset[4], formatted_amount, formatted_date, aset[7]))
            
            # Format total amounts
            formatted_total_aset = f"Rp. {int(total_aset):,}".replace(',', '.')

            conn.close()

            # Render both pemasukan and pengeluaran data in the template
            return render_template('aset.html', 
                                   aset_data=formatted_aset_data, 
                                   total_aset=formatted_total_aset,
                                   start_date=start_date, 
                                   end_date=end_date, 
                                   username=username)
        except Exception as e:
            flash(f'Error retrieving transactions: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

# @app.route('/add_aset', methods=['POST'])
def add_aset():
    if 'username' in session:
        asset_name = request.form['asset_name']
        description = request.form['description']
        owner = request.form['owner']
        category = request.form['category']
        price = request.form['price']
        purchase_date = request.form['purchase_date']
        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(purchase_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('aset' ))

        # Validate and round the price
        try:
            price = round(float(price), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('aset' ))

        # Handle image upload (if provided)
        file = request.files.get('asset_image')
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif file:
            flash('Invalid file type! Only PNG, JPG, JPEG, and GIF are allowed.', 'danger')
            return redirect(url_for('aset' ))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            

            cursor.execute("""
                INSERT INTO tbl_aset (asset_name, description, owner, category, price, purchase_date, user_id, asset_image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (asset_name, description, owner, category, price, purchase_date, session['user_id'], filename))
            
            conn.commit()
            cursor.close()
            flash('Aset berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('aset', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

# 
#@app.route('/edit_aset/<int:id>', methods=['GET', 'POST'])
def edit_aset(id):
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()

        if request.method == 'POST':
            # Ensure 'created_at' exists in the request form
            if 'purchase_date' not in request.form:
                flash('Tanggal aset tidak tersedia!', 'danger')
                return redirect(url_for('edit_aset', id=id))
               
            asset_name = request.form['asset_name']
            description = request.form['description']
            owner = request.form['owner']
            category = request.form['category']
            price = request.form['price']
            purchase_date = request.form['purchase_date']

            # Handle file upload for 'bukti_transfer'
            file = request.files.get('asset_image')
            asset_image_filename = None

            if file and allowed_file(file.filename):
                # Secure the filename
                filename = secure_filename(file.filename)
                # Save the file to the uploads folder
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                asset_image_filename = filename  # Store the filename to update in DB

            if asset_image_filename:
                cursor.execute('UPDATE tbl_aset SET asset_name = ?, description = ?, owner = ?, category = ?, price = ?, purchase_date = ?, asset_image = ? WHERE id = ?',
                               (asset_name, description, owner, category, price, purchase_date, asset_image_filename, id))
            else:
                cursor.execute('UPDATE tbl_aset SET asset_name = ?, description = ?, owner = ?, category = ?, price = ?, purchase_date = ? WHERE id = ?',
                               (asset_name, description, owner, category, price, purchase_date, id))
            conn.commit()
            conn.close()

            flash('Aset updated successfully!', 'success')
            return redirect(url_for('aset', show_collapse=True))
        else:
            cursor.execute('SELECT id, asset_name, description, owner, category, price, purchase_date, asset_image FROM tbl_aset WHERE id = ?', (id,))
            pemasukan = cursor.fetchone()
            conn.close()

            if aset:
                formatted_aset = (pemasukan[0], pemasukan[1], pemasukan[2], pemasukan[3], pemasukan[4], pemasukan[5], pemasukan[6], pemasukan[7])
                return render_template('edit_aset.html', aset=formatted_aset)
            else:
                flash('Aset not found!', 'danger')
                return redirect(url_for('aset', show_collapse=True))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))



def update_aset(id):
    if 'username' in session:
        asset_name = request.form['asset_name']
        description = request.form['description']
        owner = request.form['owner']
        category = request.form['category']
        price = request.form['price']
        purchase_date = request.form['purchase_date']

        # Validate date format (assuming YYYY-MM-DD format for SQL Server)
        try:
            datetime.strptime(purchase_date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format! Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('aset'))

        # Validate and round the price
        try:
            price = round(float(price), 2)
        except ValueError:
            flash('Invalid amount format!', 'danger')
            return redirect(url_for('aset'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tbl_aset
                SET asset_name = ?, description = ?, owner = ?, category = ?, price = ?, purchase_date = ?
                WHERE id = ?
            """, (asset_name, description, owner, category, price, purchase_date, id))
            conn.commit()
            cursor.close()
            flash('Aset updated successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('aset', show_collapse=True))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))



def delete_aset(id):
    if 'username' in session:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tbl_aset WHERE id = ?', (id,))
            conn.commit()
            cursor.close()
            flash('Aset deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('aset', show_collapse=True ))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))