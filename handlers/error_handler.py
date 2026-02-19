# handlers/error_handler.py
"""
Tratamento global de erros e anti-crash.
"""
from utils.logger import log_error
import traceback

async def setup(bot):
    @bot.event
    async def on_command_error(ctx, error):
        log_error(f"Erro em comando: {error}")
        await ctx.send(f"❌ Erro: {error}")

    @bot.event
    async def on_error(event, *args, **kwargs):
        log_error(f"Erro global: {event}\n{traceback.format_exc()}")
