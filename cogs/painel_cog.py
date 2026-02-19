import discord
from discord.ext import commands
from discord import ui
from utils.embeds import embed_bet

class PainelApostasView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.valor = None

    @ui.button(label="Criar aposta", style=discord.ButtonStyle.green, emoji="💰")
    async def criar_aposta(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CriarApostaModal())

class CriarApostaModal(ui.Modal, title="Nova Aposta"):
    valor = ui.TextInput(label="Valor da aposta (R$)", placeholder="Ex: 10, 25, 50...", required=True, min_length=1, max_length=6)
    descricao = ui.TextInput(label="Descrição (opcional)", style=discord.TextStyle.short, required=False, max_length=40)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            valor = float(self.valor.value.replace(",", "."))
            if valor <= 0:
                raise ValueError
        except Exception:
            await interaction.response.send_message(embed=embed_bet("❌ Valor inválido! Informe um número maior que zero."), ephemeral=True)
            return
        # Aqui você pode adicionar lógica para criar a aposta e parear jogadores
        await interaction.response.send_message(embed=embed_bet(f"Aposta criada: R${valor:.2f}\nAguardando adversário..."), ephemeral=True)

async def setup(bot):
    bot.add_view(PainelApostasView())
