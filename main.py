
import discord
from discord.ext import commands
import os
import asyncio
import itertools
from config.settings import DISCORD_TOKEN
from utils.logger import log_info, log_error
from handlers.command_handler import load_commands
from handlers.event_handler import load_events
from handlers.error_handler import setup as setup_error_handler
from database import setup as db_setup
from utils.branding import BOT_NAME, BOT_ICON, BOT_BANNER, BOT_BIO, BOT_DESCRIPTION

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# Evento on_ready seguro e logado
@bot.event
async def on_ready():
    log_info(f"Bot conectado como {bot.user}")
    bot.loop.create_task(dynamic_status_task())
    # Identidade visual dinâmica
    try:
        if bot.user.display_name != BOT_NAME:
            await bot.user.edit(username=BOT_NAME)
        # Avatar: só baixa se não existir localmente
        if hasattr(bot.user, "avatar") and BOT_ICON:
            import os
            if not os.path.exists("bot_avatar.png"):
                import requests
                with open("bot_avatar.png", "wb") as f:
                    f.write(requests.get(BOT_ICON).content)
            with open("bot_avatar.png", "rb") as f:
                await bot.user.edit(avatar=f.read())
    except Exception as e:
        log_error(f"[AVISO] Não foi possível atualizar nome/avatar do bot automaticamente: {e}")


# Status dinâmico
async def dynamic_status_task():
    statuses = itertools.cycle([
        discord.Activity(type=discord.ActivityType.playing, name="Free Fire | /entrar"),
        discord.Activity(type=discord.ActivityType.watching, name="Apostas seguras e rápidas!"),
        discord.Activity(type=discord.ActivityType.listening, name="/painel para apostar"),
        discord.Activity(type=discord.ActivityType.playing, name=BOT_NAME),
        discord.Activity(type=discord.ActivityType.watching, name=BOT_DESCRIPTION),
    ])
    while True:
        activity = next(statuses)
        await bot.change_presence(activity=activity, status=discord.Status.online)
        await asyncio.sleep(30)


# Carregamento seguro de comandos e eventos
async def load_all(bot):
    await load_commands(bot, os.path.join(os.path.dirname(__file__), "commands"))
    await load_events(bot, os.path.join(os.path.dirname(__file__), "events"))
    await setup_error_handler(bot)


async def main():
    try:
        db_setup()  # Setup database
        log_info("Database setup complete")
    except Exception as e:
        log_error(f"Error setting up database: {e}")
        return
    async with bot:
        await load_all(bot)
        try:
            await bot.start(DISCORD_TOKEN)
        except Exception as e:
            log_error(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
