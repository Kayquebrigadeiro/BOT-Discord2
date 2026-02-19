# helpers/embeds.py
import discord
from datetime import datetime

# Paleta de cores
COLOR_PRIMARY = 0x00E1FF  # Neon Blue
COLOR_SECONDARY = 0xA259FF  # Neon Purple
COLOR_SUCCESS = 0x00FFB0  # Neon Green
COLOR_ERROR = 0xFF3B3B  # Neon Red
COLOR_WARNING = 0xFFD600  # Neon Yellow
COLOR_BG = 0x181A20  # Dark BG

# Emojis padrão
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WAIT = "🕒"
EMOJI_BET = "💰"
EMOJI_GAME = "🎮"
EMOJI_PIX = "💳"
EMOJI_USER = "👤"
EMOJI_FIRE = "🔥"
EMOJI_ARENA = "🏟️"
EMOJI_PANEL = "🖥️"

FOOTER_TEXT = "Rockstar Bot • 2026"
FOOTER_ICON = "https://i.imgur.com/your-logo.png"  # Substitua pelo logo do bot

# Função padrão para criar embeds

def embed_base(title, description, color=COLOR_PRIMARY, thumbnail_url=None, user=None):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    elif user:
        embed.set_thumbnail(url=user.display_avatar.url)
    return embed

# Exemplos de uso:
def embed_success(msg, user=None):
    return embed_base(f"{EMOJI_SUCCESS} Sucesso!", msg, color=COLOR_SUCCESS, user=user)

def embed_error(msg, user=None):
    return embed_base(f"{EMOJI_ERROR} Erro!", msg, color=COLOR_ERROR, user=user)

def embed_wait(msg, user=None):
    return embed_base(f"{EMOJI_WAIT} Aguarde", msg, color=COLOR_SECONDARY, user=user)

def embed_bet(msg, user=None):
    return embed_base(f"{EMOJI_BET} Aposta", msg, color=COLOR_PRIMARY, user=user)
