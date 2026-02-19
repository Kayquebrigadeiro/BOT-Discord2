import discord
from discord.ext import commands
import json
from utils.encryption import decrypt_data
from models.user import Usuario  # Assuming mediadores are users with role
import logging

logging.basicConfig(filename='logs/payment.log', level=logging.INFO)

with open('config.json') as f:
    config = json.load(f)

class PaymentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Session = None

    @commands.command(name="confirmar")
    async def confirmar(self, ctx):
        # Logic for confirmation
        # Simplified
        from utils.embeds import embed_success
        msg = await ctx.send(embed=embed_success("Confirmação recebida. Enviando dados PIX..."))
        try:
            await msg.delete(delay=10)
        except Exception:
            pass
        # Calculate taxa
        valor = 10  # From context
        taxa = valor * config['taxa_percentual'] + config['taxa_fixa']
        total = valor + taxa
        # Get mediador PIX
        # Assume mediador is set
        pix_data = "Chave: 12345678900"  # Decrypted
        from utils.embeds import embed_bet
        msg2 = await ctx.send(embed=embed_bet(f"PIX: {pix_data}\nValor: R${total}"))
        try:
            await msg2.delete(delay=30)
        except Exception:
            pass

async def setup(bot):
    await bot.add_cog(PaymentCog(bot))