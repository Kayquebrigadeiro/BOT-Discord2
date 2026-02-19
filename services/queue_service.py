from database import connect

class QueueService:
    @staticmethod
    def add_to_queue(guild_id, user_id, bet_value):
        from utils.db_pool import get_conn, release_conn
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO queues (guild_id, user_id, bet_value) VALUES (?, ?, ?)",
            (guild_id, user_id, bet_value)
        )
        conn.commit()
        release_conn(conn)

    @staticmethod
    def get_queue_count(guild_id, bet_value):
        from utils.db_pool import get_conn, release_conn
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM queues WHERE guild_id=? AND bet_value=?",
            (guild_id, bet_value)
        )
        count = cursor.fetchone()[0]
        release_conn(conn)
        return count

    @staticmethod
    def get_players_in_queue(guild_id, bet_value, max_players=8):
        from utils.db_pool import get_conn, release_conn
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM queues WHERE guild_id=? AND bet_value=? ORDER BY timestamp LIMIT ?",
            (guild_id, bet_value, max_players)
        )
        players = [row[0] for row in cursor.fetchall()]
        release_conn(conn)
        return players