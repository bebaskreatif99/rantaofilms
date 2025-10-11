from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    projects = [
        {'title': 'Wedding Clip A & B', 'image': 'wedding1.jpg', 'category': 'Wedding'},
        {'title': 'Company Profile XYZ', 'image': 'company1.jpg', 'category': 'Corporate'},
        {'title': 'Short Film "Jendela"', 'image': 'film1.jpg', 'category': 'Film'},
        {'title': 'Pre-Wedding C & D', 'image': 'prewed1.jpg', 'category': 'Wedding'},
        {'title': 'Product Launch', 'image': 'product1.jpg', 'category': 'Corporate'},
        {'title': 'Music Video "Senja"', 'image': 'music1.jpg', 'category': 'Film'}
    ]
    return render_template('portfolio.html', projects=projects)

@app.route('/harga')
def price_list():
    return render_template('harga.html')

@app.route('/tentang')
def about():
    return render_template('tentang.html')

# Rute baru untuk menangani form
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Di sini Anda bisa menambahkan logika untuk mengirim email atau menyimpan ke database
        # Untuk saat ini, kita hanya akan cetak di terminal dan redirect
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Pesan Diterima:\nNama: {name}\nEmail: {email}\nPesan: {message}")
        # Redirect ke halaman 'terima kasih' atau kembali ke halaman utama
        return redirect(url_for('home'))