import discord
from discord.ext import commands, tasks
from database import connect
from utils.embeds import embed_bet

class FilasAtivasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg_id = None
        self.channel_id = None
        self.update_filas.start()

    @commands.Cog.listener()
    async def on_ready(self):
        # Defina o ID do canal de filas-ativas
        self.channel_id = ... # Coloque o ID do canal aqui
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            # Cria ou recupera a mensagem fixa
            async for msg in channel.history(limit=10):
                if msg.author == self.bot.user:
                    self.msg_id = msg.id
                    break
            if not self.msg_id:
                embed = embed_bet("🎮 Jogadores esperando\n\nAguardando apostas...")
                msg = await channel.send(embed=embed)
                self.msg_id = msg.id

    @tasks.loop(seconds=10)
    async def update_filas(self):
        if not self.channel_id or not self.msg_id:
            return
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return
        msg = await channel.fetch_message(self.msg_id)
        conn = connect()
        cursor = conn.cursor()
        # Exemplo: buscar jogadores em fila por valor
        cursor.execute("SELECT valor, user_id FROM queues ORDER BY valor")
        rows = cursor.fetchall()
        if not rows:
            embed = embed_bet("🎮 Jogadores esperando\n\nAguardando apostas...")
        else:
            valores = {}
            for valor, user_id in rows:
                valores.setdefault(valor, []).append(f"<@{user_id}>")
            desc = ""
            for valor, users in valores.items():
                desc += f"R${valor}: {', '.join(users)}\n"
            embed = embed_bet(f"🎮 Jogadores esperando\n\n{desc}")
        await msg.edit(embed=embed)
        conn.close()

async def setup(bot):
    await bot.add_cog(FilasAtivasCog(bot))
