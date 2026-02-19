from discord.ext import commands
from database import connect
from utils.logger import log

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_tax(self, ctx, tipo: str, valor: float):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO guild_config (guild_id, tax_type, tax_value)
        VALUES (?, ?, ?)
        """, (ctx.guild.id, tipo, valor))

        conn.commit()
        conn.close()

        from utils.embeds import embed_success
        msg = await ctx.send(embed=embed_success(f"Taxa configurada: {tipo} {valor}"))
        try:
            await msg.delete(delay=10)
        except Exception:
            pass
        log(f"Taxa configurada por {ctx.author}: {tipo} {valor}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_mediator(self, ctx, nome: str, pix: str, tipo: str):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO mediators (guild_id, name, pix_key, key_type)
        VALUES (?, ?, ?, ?)
        """, (ctx.guild.id, nome, pix, tipo))

        conn.commit()
        conn.close()

        from utils.embeds import embed_success
        msg = await ctx.send(embed=embed_success("Mediador adicionado com sucesso."))
        try:
            await msg.delete(delay=10)
        except Exception:
            pass
        log(f"Mediador adicionado por {ctx.author}: {nome}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))