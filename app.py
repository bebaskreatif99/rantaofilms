from flask import Flask, render_template, abort
from datetime import datetime
import contentful # Pastikan library ini sudah diinstal
import os

app = Flask(__name__)

# --- Mengambil Kunci API dari Environment Variables Vercel ---
SPACE_ID = os.environ.get('CONTENTFUL_SPACE_ID')
DELIVERY_API_KEY = os.environ.get('CONTENTFUL_DELIVERY_API_KEY')

# --- Inisialisasi Klien Contentful ---
client = None
if SPACE_ID and DELIVERY_API_KEY:
    try:
        client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)
    except Exception as e:
        print(f"Error: Gagal terhubung ke Contentful. Periksa kunci API Anda. Detail: {e}")
else:
    print("Error: Variabel CONTENTFUL_SPACE_ID atau CONTENTFUL_DELIVERY_API_KEY tidak ditemukan.")

# =====================================================================
# FUNGSI BANTUAN
# =====================================================================
def map_project_entry(entry):
    """Fungsi ini menerjemahkan data dari Contentful ke format yang dimengerti HTML kita."""
    fields = entry.fields()
    # PENTING: Nama field di sini (misal: 'cover_image') harus SAMA PERSIS dengan Field ID di Contentful.
    return {
        'id': entry.sys['id'],
        'slug': fields.get('slug', entry.sys['id']),
        'title': fields.get('title', 'Tanpa Judul'),
        'description': fields.get('description'),
        'category': fields.get('category', 'Tanpa Kategori'),
        'cover_image': fields.get('cover_image').url() if fields.get('cover_image') else None,
        'project_date': fields.get('project_date'),
        'video_url': fields.get('video_url'),
        'is_featured': fields.get('is_featured', False),
    }

@app.context_processor
def inject_global_vars():
    return {
        'current_year': datetime.utcnow().year,
        'site': {
            "instagram_url": "https://www.instagram.com/NAMA_INSTAGRAM_ANDA",
            "tiktok_url": "https://www.tiktok.com/@NAMA_TIKTOK_ANDA",
            "whatsapp_url": "https://wa.me/6281234567890",
            "logo": "img/logo.png",
            "team_photo": "img/tim-rantaofilms.png"
        }
    }

# =====================================================================
# RUTE APLIKASI
# =====================================================================
@app.route('/')
def home():
    if not client: return "Error: Koneksi ke CMS gagal. Periksa log Vercel.", 500
    
    featured_projects = []
    try:
        featured_entries = client.entries({
            'content_type': 'project', # Pastikan ID Content Type Anda adalah 'project'
            'fields.is_featured': True
        })
        featured_projects = [map_project_entry(entry) for entry in featured_entries]
    except Exception as e:
        print(f"Error saat mengambil data 'featured': {e}")
        
    return render_template('index.html', featured_projects=featured_projects)

@app.route('/portfolio')
def portfolio():
    if not client: return "Error: Koneksi ke CMS gagal. Periksa log Vercel.", 500
    
    all_projects = []
    try:
        all_entries = client.entries({'content_type': 'project'})
        all_projects = [map_project_entry(entry) for entry in all_entries]
    except Exception as e:
        print(f"Error saat mengambil semua proyek: {e}")
    
    categories = sorted(list(set(p['category'] for p in all_projects if p.get('category'))))
    return render_template('portfolio.html', projects=all_projects, categories=categories)

# ... Rute statis lainnya tidak berubah ...
@app.route('/harga')
def price_list(): return render_template('harga.html')

@app.route('/tentang')
def about(): return render_template('tentang.html')

@app.route('/kontak', methods=['GET', 'POST']): # Rute kontak tidak perlu diubah
    pass

@app.errorhandler(404)
def page_not_found(e): return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

