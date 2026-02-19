from database import connect

class MatchService:
    @staticmethod
    def create_match(guild_id, player1, player2, bet_value, channel_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO matches (guild_id, player1, player2, bet_value, status, channel_id) VALUES (?, ?, ?, ?, ?, ?)",
            (guild_id, player1, player2, bet_value, 'waiting', channel_id)
        )
        match_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return match_id

    @staticmethod
    def update_match_status(match_id, status):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE matches SET status=? WHERE id=?",
            (status, match_id)
        )
        conn.commit()
        conn.close()