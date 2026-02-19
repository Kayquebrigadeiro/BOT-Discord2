import sqlite3
import threading

# Pool de conexões simples para SQLite
class SQLiteConnectionPool:
    def __init__(self, db_path, maxsize=10):
        self.db_path = db_path
        self.maxsize = maxsize
        self._pool = []
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            if self._pool:
                return self._pool.pop()
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def put(self, conn):
        with self._lock:
            if len(self._pool) < self.maxsize:
                self._pool.append(conn)
            else:
                conn.close()

# Instância global do pool
pool = SQLiteConnectionPool("database.db", maxsize=20)

def get_conn():
    return pool.get()

def release_conn(conn):
    pool.put(conn)

def setup():
    conn = get_conn()
    cursor = conn.cursor()
    # ... (restante igual ao setup atual)
    # (copie o conteúdo do setup antigo aqui, usando conn/cursor)
    conn.commit()
    release_conn(conn)
