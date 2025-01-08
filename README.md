# Kaiadmin Lite - Free Bootstrap 5 Admin Dashboard
![kaiadminlitethumb (1)](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/4793c6b9-7991-4502-8633-14d9ed0ea486)

This time, I want to introduce you Kaiadmin Lite – a free Bootstrap 5 Admin Dashboard built to easily manage and visualize business data.

With Kaiadmin Lite, you can complete development faster with no design skills required. Save 1000s of hours of designing and coding work, as we've already done that for you.

Don't worry about getting started – we've documented how to get started using this dashboard template and utilizing the available components and plugins, making it easy to leverage the full potential of Kaiadmin Bootstrap 5 Admin Dashboard.

**Product Detail** : https://themekita.com/kaiadmin-lite-bootstrap-5-dashboard.html

**Live Preview** : https://themekita.com/demo-kaiadmin-lite-bootstrap-dashboard/livepreview/demo1/

# Get Kaiadmin PRO

![bg_themekitacom](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/195bfcb3-f587-4920-bfba-a583244116ad)
[Product Detail](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/) |  [Buy This](https://themekita.lemonsqueezy.com/buy/526b603e-8eb3-4dcb-a7a3-842375952df5)

***
### [Kaiadmin - Classic Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo1/)
![Kaiadmin - Classic Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/106e027a-4ffe-4856-b729-0e6939c0473d)

***
### [Kaiadmin - White Classic Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo2/)
![Kaiadmin - White Classic Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/ab70a0f7-116d-46ad-9037-a4081b0db763)

***
### [Kaiadmin - Dark Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo3/)
![Kaiadmin - Dark Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/1a645dc4-d150-45d7-9883-1955b0666d18)

***
### [Kaiadmin - Creative Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo4/)
![Kaiadmin - Creative Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/fccc0204-3cb7-45dd-b0a5-532c57af3c12)

***
### [Kaiadmin - Trendy Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo5/)
![Kaiadmin - Trendy Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/bd9d4ce8-08a3-48bd-975e-3d77e5c51388)

***
### [Kaiadmin - Trendy 2 Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo6/)
![Kaiadmin - Trendy 2 Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/3cdd531f-16e0-4c4e-bfbd-89f80d3a25fe)

***
### [Kaiadmin - Horizontal Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo7/)
![Kaiadmin - Horizontal Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/2cac93cc-2542-43d9-9072-8625bdd2f8ad)

***
### [Kaiadmin - Enterprise Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo8/)
![Kaiadmin - Enterprise Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/ce2aa3f8-1f62-4ca1-87cd-111b74e50940)

***
### [Kaiadmin - Futuristic Dashboard](https://themekita.com/demo-kaiadmin-pro-bootstrap-dashboard/livepreview/examples/demo9/)
![Kaiadmin - Futuristic Dashboard](https://github.com/Hizrian/kaiadmin-lite/assets/10692084/83f79f3d-d248-4d01-ac15-9c98bee3ca9f)



2. Instalasi Library yang Diperlukan
Pastikan Anda telah menginstal Flask dan pyodbc untuk menghubungkan ke SQL Server. Anda dapat menginstalnya dengan pip:

bash
Copy code
pip install Flask pyodbc flask-login


.\venv\Scripts\activate

python app.py


pip install bcrypt


=========================================================
Database
=========================================================

/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP 1000 [id]
      ,[username]
      ,[password]
      ,[email]
	  ,[role]
  FROM [bukukas].[dbo].[users]


UPDATE [bukukas].[dbo].[users]
SET 
    [username] = 'admin',
    [password] = '$2a$10$xH0vzmi1e4ozhEMRqTcLEOWeGKhRh7rjw6QR0zHAdVQDULl0rEW5S',
	[email] = 'admin@bukukas.com',
	[role] = 'admin'
WHERE [id] = 1;


CREATE TABLE pemasukan (
    id INT PRIMARY KEY IDENTITY(1,1),
    amount DECIMAL(18, 2) NOT NULL,
    description NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from pemasukan

CREATE TABLE pengeluaran (
    id INT PRIMARY KEY IDENTITY(1,1),
    amount DECIMAL(18, 2) NOT NULL,
    description NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

select * from pengeluaran




=========================================================
Plugin
=========================================================
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\core\jquery-3.7.1.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\core\popper.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\core\bootstrap.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\webfont\webfont.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\bootstrap-notify\bootstrap-notify.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\bootstrap-tagsinput\bootstrap-tagsinput.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\bootstrap-toggle\bootstrap-toggle.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\chart-circle\chart-circle.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\chart.js\chart.js.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\datatables\datatables.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\datepicker\datepicker.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\dropzone\dropzone.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\fullcalendar\fullcalendar.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\gmaps\gmaps.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\jquery-scrollbar\jquery-scrollbar.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\jquery.magnific-popup\jquery.magnific-popup.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\jquery.sparkline\jquery.sparkline.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\jquery.validate\jquery.validate.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\jsvectormap\jsvectormap.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\list.js\list.js.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\moment\moment.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\owl-carousel\owl-carousel.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\select2\select2.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\sortable\sortable.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\sticky-sidebar\sticky-sidebar.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\summernote\summernote.min.js"></script>
    <script src="../static\kaiadmin-lite-1.2.0\assets\js\plugin\sweetalert\sweetalert.min.js"></script>


    <link href="../static\kaiadmin-lite-1.2.0\assets\css\bootstrap.min.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\demo.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\fonts.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\fonts.min.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\kaiadmin.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\kaiadmin.min.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\plugins.css" rel="stylesheet">
    <link href="../static\kaiadmin-lite-1.2.0\assets\css\plugins.min.css" rel="stylesheet">





@app.route('/transaksi')
@app.route('/add_pemasukan', methods=['POST'])
@app.route('/edit_pemasukan/<int:id>', methods=['GET'])
@app.route('/update_pemasukan/<int:id>', methods=['POST'])




@app.route('/tabungan_mandiri')
@app.route('/add_tabungan_mandiri', methods=['POST'])
@app.route('/edit_tabungan_mandiri/<int:id>', methods=['GET'])
@app.route('/update_tabungan_mandiri/<int:id>', methods=['POST'])
@app.route('/delete_tabungan_mandiri/<int:id>', methods=['POST'])


Fold All: Untuk menyembunyikan semua blok kode sekaligus, tekan Ctrl + K, lalu Ctrl + 0.

Unfold All: Untuk menampilkan kembali semua blok kode, tekan Ctrl + K, lalu Ctrl + J.



- upload bukti transfer
- sort by kolom




@app.route('/transaksi', methods=['GET'])
def transaksi():
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
            formatted_total_pemasukan = f"Rp. {int(total_pemasukan):,}".replace(',', '.')
            formatted_total_pengeluaran = f"Rp. {int(total_pengeluaran):,}".replace(',', '.')

            conn.close()

            # Render both pemasukan and pengeluaran data in the template
            return render_template('transaksi.html', 
                                   pemasukan_data=formatted_pemasukan_data, 
                                   total_pemasukan=formatted_total_pemasukan,
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











