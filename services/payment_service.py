from database import connect

def calculate_tax(guild_id, bet_value):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT tax_type, tax_value FROM guild_config WHERE guild_id=?", (guild_id,))
    config = cursor.fetchone()

    if not config:
        return 0

    tax_type, tax_value = config

    if tax_type == "fixed":
        tax = tax_value
    else:
        tax = bet_value * (tax_value / 100)

    conn.close()
    return round(tax, 2)


def get_active_mediator(guild_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name, pix_key FROM mediators WHERE guild_id=? AND active=1 LIMIT 1", (guild_id,))
    mediator = cursor.fetchone()

    conn.close()
    return mediator