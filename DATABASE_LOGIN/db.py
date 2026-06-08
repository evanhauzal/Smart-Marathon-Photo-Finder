"""
Database connection and initialization module.
Uses PostgreSQL for user authentication and role management only.
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "Falah123",
    "dbname": "marathon_db",
}


def get_connection():
    """Get a new database connection."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def init_db():
    """
    Initialize the database.
    Creates the marathon_db database if it doesn't exist,
    then creates the users table.
    """
    # First connect without specifying a database to create the DB if needed
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG["dbname"],)
        )
        if not cursor.fetchone():
            cursor.execute(f'CREATE DATABASE {DB_CONFIG["dbname"]}')
            print(f"Database '{DB_CONFIG['dbname']}' created.")
        else:
            print(f"Database '{DB_CONFIG['dbname']}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

    # Now connect to the database and create tables
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('USER', 'PHOTOGRAPHER')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Error initializing tables: {e}")
        raise
