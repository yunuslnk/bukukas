from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import get_db_connection  # Ensure you have a valid database connection function in config.py
import bcrypt

app = Flask(__name__)
app.secret_key = 'secret123'  # Encryption key for sessions

# Route for login
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
            session['role'] = user[3]  # Store role in session (e.g., 'admin' or 'user')
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!', 'danger')

    return render_template('login.html')


# Route for the main page (home)
@app.route('/')
def home():
    if 'username' in session:  # Check if user is logged in
        return render_template('home.html', role=session['role'])
    return redirect(url_for('login'))


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Route for showing data (only for admins)
@app.route('/data')
def show_data():
    if 'role' in session and session['role'] == 'admin':  # Check if the user is an admin
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')  # Show all users data
        data = cursor.fetchall()
        conn.close()
        return render_template('data.html', data=data)
    else:
        flash('You do not have permission to view this page!', 'danger')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)  # Run Flask in debug mode
