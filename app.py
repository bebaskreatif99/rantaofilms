from flask import Flask, render_template, abort, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# =====================================================================
# DATA SIMULASI (Pengganti Database)
# =====================================================================

site_data = {
    "instagram_url": "https://www.instagram.com/NAMA_INSTAGRAM_ANDA",
    "tiktok_url": "https://www.tiktok.com/@NAMA_TIKTOK_ANDA",
    "whatsapp_url": "https://wa.me/6281234567890", # Ganti dengan nomor Anda
    "logo": "img/logo.png",
    "team_photo": "img/tim-rantaofilms.png"
}

projects_data = [
    {
        "id": 1, "slug": "penantian-yang-indah-wedding", "title": "Penantian yang Indah",
        "description": "Sebuah perayaan cinta yang sakral dan intim, menangkap setiap tatapan penuh makna dan senyum bahagia dari pasangan mempelai. Konsep sinematik dengan sentuhan hangat dan natural.",
        "category": "Wedding", "cover_image": "img/portfolio/wedding-1.jpg",
        "project_date": "15 Agustus 2025", "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "images": ["img/portfolio/wedding-1-gallery-1.jpg", "img/portfolio/wedding-1-gallery-2.jpg"],
        "is_featured": True,
    },
    {
        "id": 2, "slug": "senja-di-atas-awan-prewedding", "title": "Senja di Atas Awan",
        "description": "Kisah cinta yang dilukis oleh alam. Sesi pre-wedding di puncak bukit, menangkap siluet romantis dengan latar belakang matahari terbenam yang dramatis.",
        "category": "Pre-Wedding", "cover_image": "img/portfolio/prewed-1.jpg",
        "project_date": "20 Juli 2025", "video_url": None,
        "images": ["img/portfolio/prewed-1-gallery-1.jpg"], "is_featured": True,
    },
    {
        "id": 3, "slug": "langkah-baru-graduation", "title": "Langkah Baru",
        "description": "Merayakan akhir dari sebuah perjuangan dan awal dari petualangan baru. Sesi foto wisuda yang ceria dan penuh harapan bersama keluarga tercinta.",
        "category": "Graduation", "cover_image": "img/portfolio/graduation-1.jpg",
        "project_date": "10 September 2025", "video_url": None, "images": [], "is_featured": False,
    },
    {
        "id": 4, "slug": "energi-nusantara-event", "title": "Energi Nusantara",
        "description": "Dokumentasi lengkap dari acara gathering korporat tahunan, menangkap semangat kolaborasi, pidato inspiratif, dan momen kebersamaan tim.",
        "category": "Event", "cover_image": "img/portfolio/event-1.jpg",
        "project_date": "05 Juni 2025", "video_url": None, "images": [], "is_featured": True,
    },
    {
        "id": 5, "slug": "rasa-kopi-nusantara-branding", "title": "Rasa Kopi Nusantara",
        "description": "Visual branding untuk produk kopi lokal, menampilkan kehangatan dan kekayaan cita rasa asli Indonesia.",
        "category": "Branding", "cover_image": "img/portfolio/branding-1.jpg",
        "project_date": "01 Mei 2025", "video_url": None, "images": [], "is_featured": False,
    },
]

# =====================================================================
# FUNGSI BANTUAN (Context Processor)
# =====================================================================
@app.context_processor
def inject_global_vars():
    return {
        'current_year': datetime.utcnow().year,
        'site': site_data
    }

# =====================================================================
# RUTE APLIKASI (Controller)
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

# --- PERBAIKAN DI BARIS DI BAWAH INI ---
@app.route('/kontak', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Pesan Baru Diterima dari {name} ({email}):\n{message}")
        return render_template('kontak_sukses.html')
    return render_template('kontak.html')
# --- AKHIR PERBAIKAN ---
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)