from flask import Flask, render_template, abort, request
from datetime import datetime

app = Flask(__name__)

# =====================================================================
# DATA "DATABASE" MANUAL ANDA
# SEMUA PORTFOLIO DIKELOLA DI SINI
# =====================================================================

site_data = {
    "instagram_url": "https://www.instagram.com/NAMA_INSTAGRAM_ANDA",
    "tiktok_url": "https://www.tiktok.com/@NAMA_TIKTOK_ANDA",
    "whatsapp_url": "https://wa.me/6281234567890", # Ganti dengan nomor Anda
    "logo": "img/logo.png",
    "team_photo": "img/tim-rantaofilms.png"
}

# --- UNTUK MENAMBAH PROYEK BARU, SALIN-TEMPEL BLOK DI BAWAH INI ---
projects_data = [
    # --- PROYEK WISUDA BARU ---
    {
        "id": 6, "slug": "langkah-menuju-masa-depan-graduation", "title": "Langkah Menuju Masa Depan",
        "description": "Mengabadikan senyum bahagia dan rasa syukur di hari kelulusan. Sesi foto ini menangkap esensi dari sebuah pencapaian penting dan awal dari perjalanan baru yang gemilang, penuh harapan dan optimisme.",
        "category": "Graduation",
        "cover_image": "img/portfolio/graduation (6).jpg", # Gambar sampul untuk halaman utama/portofolio
        "project_date": "12 Oktober 2025",
        "video_url": None, # Jika ada video, ganti None dengan link YouTube/Vimeo embed
        "images": [ # Daftar semua gambar untuk galeri di halaman detail
            "img/portfolio/graduation (1).jpg",
            "img/portfolio/graduation (2).jpg",
            "img/portfolio/graduation (3).jpg",
            "img/portfolio/graduation (4).jpg",
            "img/portfolio/graduation (5).jpg",
            "img/portfolio/graduation (7).jpg",
            "img/portfolio/graduation (8).jpg",
            "img/portfolio/graduation (9).jpg"
        ],
        "is_featured": True, # Atur True jika ingin tampil di halaman utama
    },
]

# =====================================================================
# FUNGSI BANTUAN
# =====================================================================
@app.context_processor
def inject_global_vars():
    return {
        'current_year': datetime.utcnow().year,
        'site': site_data
    }

# =====================================================================
# RUTE APLIKASI
# =====================================================================
@app.route('/')
def home():
    featured_projects = [p for p in projects_data if p['is_featured']]
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/portfolio')
def portfolio():
    categories = sorted(list(set(p['category'] for p in projects_data)))
    return render_template('portfolio.html', projects=projects_data, categories=categories)

@app.route('/portfolio/<slug>')
def portfolio_detail(slug):
    project = next((p for p in projects_data if p['slug'] == slug), None)
    if project is None: abort(404)
    return render_template('portfolio_detail.html', project=project)

@app.route('/harga')
def price_list():
    return render_template('harga.html')

@app.route('/tentang')
def about():
    return render_template('tentang.html')

@app.route('/kontak', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Pesan Baru Diterima dari {name} ({email}):\n{message}")
        return render_template('kontak_sukses.html')
    return render_template('kontak.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
