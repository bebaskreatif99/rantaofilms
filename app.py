from flask import Flask, render_template, abort, request
from datetime import datetime

app = Flask(__name__)

# =====================================================================
# DATA "DATABASE" MANUAL ANDA
# =====================================================================

site_data = {
    "instagram_url": "https://www.instagram.com/andreesnrt_",
    "tiktok_url": "https://www.tiktok.com/andreesnrt",
    "whatsapp_url": "https://wa.me/6281354704624", # Ganti dengan nomor Anda
    "logo": "img/logo.png",
    "team_photo": "img/tim-rantaofilms.png"
}

projects_data = [
    {
        "id": 7, "slug": "elegansi-dalam-hening-wedding", "title": "Elegansi dalam Hening",
        "description": "Sebuah potret pernikahan yang menangkap keindahan dan ketenangan momen sakral. Dengan pencahayaan dramatis dan fokus pada detail, setiap foto menceritakan kisah keanggunan yang tak lekang oleh waktu.",
        "category": "Wedding",
        "cover_image": "img/portfolio/wedding-04.jpg", # NAMA FILE BARU
        "project_date": "18 Oktober 2025",
        "video_url": None,
        "images": [
            "img/portfolio/wedding-01.jpg", # NAMA FILE BARU
            "img/portfolio/wedding-02.jpg", # NAMA FILE BARU
            "img/portfolio/wedding-03.jpg"  # NAMA FILE BARU
        ],
        "is_featured": True,
    },
    {
        "id": 6, "slug": "langkah-menuju-masa-depan-graduation", "title": "Langkah Menuju Masa Depan",
        "description": "Mengabadikan senyum bahagia dan rasa syukur di hari kelulusan. Sesi foto ini menangkap esensi dari sebuah pencapaian penting dan awal dari perjalanan baru yang gemilang, penuh harapan dan optimisme.",
        "category": "Graduation",
        "cover_image": "img/portfolio/graduation-06.jpg", # NAMA FILE BARU
        "project_date": "12 Oktober 2025", "video_url": None,
        "images": [
            "img/portfolio/graduation-01.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-02.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-03.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-04.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-05.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-07.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-08.jpg", # NAMA FILE BARU
            "img/portfolio/graduation-09.jpg"  # NAMA FILE BARU
        ],
        "is_featured": True,
    },
    # Proyek lama lainnya (jika ada, ubah juga nama filenya)
]

# =====================================================================
# FUNGSI BANTUAN & RUTE (Tidak ada perubahan di bawah ini)
# =====================================================================
@app.context_processor
def inject_global_vars():
    return {
        'current_year': datetime.utcnow().year,
        'site': site_data
    }

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