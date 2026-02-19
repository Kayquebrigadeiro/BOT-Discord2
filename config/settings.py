# config/settings.py
# Centraliza configurações sensíveis e variáveis de ambiente
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Adicione outras configs conforme necessário
