from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import get_db_connection
from datetime import datetime, timedelta

# Transaksi asset
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

            # Fetch aset (income) data
            query_aset = '''SELECT id, asset_name, description, owner, category, price, purchase_date, asset_image 
                                 FROM tbl_aset 
                                 WHERE user_id = ?'''
            params_aset = [session['user_id']]

            if start_date and end_date:
                query_aset += ' AND created_at BETWEEN ? AND ?'
                params_aset.extend([start_date, end_date])

            cursor.execute(query_aset, params_aset)
            aset_data = cursor.fetchall()

            # Calculate total aset
            total_aset = sum(aset[1] for aset in aset_data)

            # Format aset data
            formatted_aset_data = []
            for aset in aset_data:
                formatted_date = aset[3].strftime('%d-%m-%Y')
                formatted_amount = f"Rp. {int(aset[1]):,}".replace(',', '.')
                formatted_aset_data.append((aset[0], formatted_amount, aset[2], formatted_date, aset[4]))

            # Format total amounts
            formatted_total_aset = f"Rp. {int(total_aset):,}".replace(',', '.')

            conn.close()

            # Render aset data in the template
            return render_template('aset.html',
                                   aset_data=formatted_aset_data,
                                   total_aset=formatted_total_aset,
                                   start_date=start_date,
                                   end_date=end_date,
                                   username=username)
        except Exception as e:
            flash(f'Error retrieving assets: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))
