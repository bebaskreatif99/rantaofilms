from flask import Flask, render_template

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Rute untuk halaman utama (Landing Page)
@app.route('/')
def home():
    # 'index.html' harus ada di dalam folder 'templates'
    return render_template('index.html')

# Rute untuk halaman Portfolio
@app.route('/portfolio')
def portfolio():
    # Di sini nanti Anda bisa menambahkan data proyek dari database atau file
    projects = [
        {'title': 'Wedding Clip A & B', 'image': 'wedding1.jpg', 'category': 'Wedding'},
        {'title': 'Company Profile XYZ', 'image': 'company1.jpg', 'category': 'Corporate'},
        {'title': 'Short Film "Jendela"', 'image': 'film1.jpg', 'category': 'Film'}
    ]
    return render_template('portfolio.html', projects=projects)

# Rute untuk halaman Price List
@app.route('/harga')
def price_list():
    return render_template('harga.html')

# Rute untuk halaman Tentang
@app.route('/tentang')
def about():
    return render_template('tentang.html')

# Ini opsional, hanya untuk menjalankan di komputer lokal
if __name__ == '__main__':
    app.run(debug=True)