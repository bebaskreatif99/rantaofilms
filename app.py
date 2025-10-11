from flask import Flask, render_template, abort
from datetime import datetime
import contentful # Library baru untuk koneksi ke Contentful

app = Flask(__name__)

# --- Kunci API dari Contentful ---
# (Kita akan menyimpannya di Vercel, bukan di sini)
import os
SPACE_ID = os.environ.get('CONTENTFUL_SPACE_ID')
DELIVERY_API_KEY = os.environ.get('CONTENTFUL_DELIVERY_API_KEY')

# --- Inisialisasi Klien Contentful ---
try:
    client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)
except Exception as e:
    client = None
    print(f"Error initializing Contentful client: {e}")

# =====================================================================
# FUNGSI BANTUAN
# =====================================================================
def map_project_entry(entry):
    """Mengubah format data dari Contentful agar sesuai dengan template kita."""
    fields = entry.fields()
    return {
        'id': entry.sys['id'],
        'slug': fields.get('slug', entry.sys['id']), # Asumsi ada field slug
        'title': fields.get('title'),
        'description': fields.get('description'),
        'category': fields.get('category'),
        'cover_image': fields.get('cover_image').url() if fields.get('cover_image') else None,
        'project_date': fields.get('project_date'),
        'video_url': fields.get('video_url'),
        'is_featured': fields.get('is_featured', False),
    }

@app.context_processor
def inject_global_vars():
    # Ambil data global dari CMS jika ada, atau gunakan default
    return {
        'current_year': datetime.utcnow().year,
        'site': {
            "instagram_url": "https://www.instagram.com/NAMA_INSTAGRAM_ANDA",
            "tiktok_url": "https://www.tiktok.com/@NAMA_TIKTOK_ANDA",
            "whatsapp_url": "https://wa.me/6281234567890",
            "logo": "img/logo.png", # Logo tetap file statis
            "team_photo": "img/tim-rantaofilms.png"
        }
    }

# =====================================================================
# RUTE APLIKASI
# =====================================================================
@app.route('/')
def home():
    if not client: return "Error: Cannot connect to Contentful.", 500
    
    # Ambil proyek yang is_featured = true dari Contentful
    featured_entries = client.entries({
        'content_type': 'project', # Sesuaikan dengan ID Content Type Anda
        'fields.is_featured': True
    })
    featured_projects = [map_project_entry(entry) for entry in featured_entries]
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/portfolio')
def portfolio():
    if not client: return "Error: Cannot connect to Contentful.", 500
    
    all_entries = client.entries({'content_type': 'project'})
    all_projects = [map_project_entry(entry) for entry in all_entries]
    
    categories = sorted(list(set(p['category'] for p in all_projects if p['category'])))
    return render_template('portfolio.html', projects=all_projects, categories=categories)

# Rute lain (harga, tentang, kontak) tetap sama karena kontennya statis
@app.route('/harga')
def price_list():
    return render_template('harga.html')

@app.route('/tentang')
def about():
    return render_template('tentang.html')

@app.route('/kontak', methods=['GET', 'POST']):
    # ... (logika kontak tidak berubah)
    pass
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Untuk testing lokal, Anda perlu set environment variables di terminal dulu
    app.run(debug=True)