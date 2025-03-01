from flask import render_template, flash, session, redirect, url_for

# Fungsi untuk menangani route /template
def show_template():
    if 'role' in session and session['role'] == 'admin':  # Cek apakah user adalah admin
        username = session['username']
        return render_template('template.html', username=username)
    else:
        flash('You do not have permission to view this page!', 'danger')
        return redirect(url_for('home'))
