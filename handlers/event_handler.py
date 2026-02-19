# handlers/event_handler.py
"""
Carrega e registra todos os eventos de forma segura e modular.
"""
import importlib
import os
from utils.logger import log_info, log_error

async def load_events(bot, events_path: str):
    for filename in os.listdir(events_path):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = f"events.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "setup"):
                    await module.setup(bot)
                    log_info(f"Evento carregado: {filename}")
            except Exception as e:
                log_error(f"Erro ao carregar evento {filename}: {e}")
