def connect():

from utils.db_pool import get_conn, release_conn

def setup():
    conn = get_conn()
    cursor = conn.cursor()

    # Filas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        user_id INTEGER UNIQUE,
        bet_value INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Partidas (agora suporta times até 4v4)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        team1 TEXT, -- JSON: lista de user_ids
        team2 TEXT, -- JSON: lista de user_ids
        bet_value INTEGER,
        status TEXT,
        channel_id INTEGER,
        confirmations TEXT, -- JSON: dict user_id:bool
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Mediadores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mediators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        name TEXT,
        pix_key TEXT,
        key_type TEXT,
        active INTEGER DEFAULT 1
    )
    """)

    # Configuração do servidor
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id INTEGER PRIMARY KEY,
        tax_type TEXT,
        tax_value REAL
    )
    """)

    # Blacklist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blacklist (
        user_id INTEGER PRIMARY KEY,
        reason TEXT
    )
    """)

    conn.commit()
    release_conn(conn)