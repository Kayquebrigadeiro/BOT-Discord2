import discord
from discord import app_commands
from discord.ext import commands
import json
from models.user import Usuario
import logging

logging.basicConfig(filename='logs/admin.log', level=logging.INFO)

with open('config.json') as f:
    config = json.load(f)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Session = None

    @app_commands.command(name="add_mediador", description="Adicionar mediador")
    @app_commands.describe(user="Usuário", chave_pix="Chave PIX", cpf="CPF", email="Email", nome="Nome", tipo="Tipo de chave")
    async def add_mediador(self, interaction: discord.Interaction, user: discord.Member, chave_pix: str, cpf: str, email: str, nome: str, tipo: str):
        # Check permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Permissões insuficientes!", ephemeral=True)
            return
        # Add to DB
        session = self.Session()
        mediador = Usuario(discord_id=str(user.id), nome=nome)  # Extend model for mediador fields
        # Add encrypted fields
        session.add(mediador)
        session.commit()
        session.close()
        await interaction.response.send_message("Mediador adicionado!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))