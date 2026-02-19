import discord
from discord.ext import commands, tasks
from database import connect
from utils.embeds import embed_bet

class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg_id = None
        self.channel_id = None
        self.update_ranking.start()

    @commands.Cog.listener()
    async def on_ready(self):
        # Defina o ID do canal de ranking
        self.channel_id = ... # Coloque o ID do canal aqui
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            # Cria ou recupera a mensagem fixa
            async for msg in channel.history(limit=10):
                if msg.author == self.bot.user:
                    self.msg_id = msg.id
                    break
            if not self.msg_id:
                embed = embed_bet("🏆 Ranking\n\nAguardando partidas...")
                msg = await channel.send(embed=embed)
                self.msg_id = msg.id

    @tasks.loop(seconds=30)
    async def update_ranking(self):
        if not self.channel_id or not self.msg_id:
            return
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return
        msg = await channel.fetch_message(self.msg_id)
        conn = connect()
        cursor = conn.cursor()
        # Exemplo: buscar top 10 jogadores por vitórias
        cursor.execute("SELECT user_id, COUNT(*) as vitorias FROM matches WHERE status='win' GROUP BY user_id ORDER BY vitorias DESC LIMIT 10")
        rows = cursor.fetchall()
        if not rows:
            embed = embed_bet("🏆 Ranking\n\nAguardando partidas...")
        else:
            desc = ""
            for i, (user_id, vitorias) in enumerate(rows, 1):
                desc += f"{i}. <@{user_id}> — {vitorias} vitórias\n"
            embed = embed_bet(f"🏆 Top 10 Jogadores\n\n{desc}")
        await msg.edit(embed=embed)
        conn.close()

async def setup(bot):
    await bot.add_cog(RankingCog(bot))
