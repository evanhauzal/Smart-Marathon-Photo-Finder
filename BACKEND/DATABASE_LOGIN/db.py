"""
Database connection and initialization module for Supabase.
Uses Supabase client for user authentication and role management.
"""

from supabase import create_client, Client

# Konfigurasi Supabase Anda
SUPABASE_URL = "https://dsnxpqswqmceashckexz.supabase.co"
SUPABASE_KEY = "sb_secret_lIoTQLlVhCFsZuyHC8Dkjg_UoH2ozOd"

def get_supabase_client() -> Client:
    """Get a Supabase client instance."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def init_db():
    """
    Initialize the database by creating the users table if it doesn't exist.
    Executes the SQL schema directly through the Supabase RPC/SQL interface.
    """
    supabase = get_supabase_client()
    
    # Query SQL untuk membuat tabel users
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('USER', 'PHOTOGRAPHER')),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        # Menjalankan query SQL langsung menggunakan fungsi eksekusi bawaan Supabase
        supabase.postgrest.rpc("exec_sql", {"sql_query": create_table_query}).execute()
        print("Database tables initialized successfully via Python.")
    except Exception as e:
        # Jika fungsi exec_sql belum terkonfigurasi di Supabase RPC, 
        # kita tampilkan pesan log atau gunakan alternatif penanganan error.
        print(f"Catatan: Pastikan ekstensi atau fungsi pembantu SQL sudah diizinkan, atau buat tabel langsung di SQL Editor Dashboard Supabase jika terjadi kendala akses. Error rincian: {e}")