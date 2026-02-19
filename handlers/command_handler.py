# handlers/command_handler.py
"""
Carrega e registra todos os comandos de forma segura e modular.
"""
import importlib
import os
from discord.ext import commands
from utils.logger import log_info, log_error

async def load_commands(bot: commands.Bot, commands_path: str):
    for filename in os.listdir(commands_path):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = f"commands.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "setup"):
                    await module.setup(bot)
                    log_info(f"Comando carregado: {filename}")
            except Exception as e:
                log_error(f"Erro ao carregar comando {filename}: {e}")
