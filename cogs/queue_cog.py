
from discord.ext import commands
import discord
import asyncio
from database import connect
from services.queue_service import QueueService
from services.match_service import MatchService
from services.security_service import SecurityService
from utils.match_view import ConfirmView
from utils.logger import log

class QueueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="entrar", description="Entrar em uma fila de aposta")
    @discord.app_commands.describe(valor="Valor da aposta (ex: 1, 2, 5, 10)")
    async def entrar(self, interaction: discord.Interaction, valor: int):
        user = interaction.user
        guild = interaction.guild
        conn = connect()
        cursor = conn.cursor()

        # Blacklist check
        cursor.execute("SELECT * FROM blacklist WHERE user_id=?", (user.id,))
        if cursor.fetchone():
            from utils.embeds import embed_error
            await interaction.response.defer(thinking=True, ephemeral=True)
            await interaction.followup.send(embed=embed_error("Você está bloqueado de usar o sistema.", user), ephemeral=True)
            conn.close()
            return

        # Multi-fila check
        cursor.execute("SELECT * FROM queues WHERE user_id=?", (user.id,))
        if cursor.fetchone():
            from utils.embeds import embed_error
            await interaction.response.defer(thinking=True, ephemeral=True)
            await interaction.followup.send(embed=embed_error("Você já está em uma fila.", user), ephemeral=True)
            conn.close()
            return

        QueueService.add_to_queue(guild.id, user.id, valor)
        from utils.embeds import embed_success
        await interaction.response.defer(thinking=True, ephemeral=True)
        await interaction.followup.send(embed=embed_success(f"Você entrou na fila de R${valor}! Aguarde o pareamento...", user), ephemeral=True)

        jogadores = QueueService.get_players_in_queue(guild.id, valor, max_players=8)

        if len(jogadores) >= 2:
            # Permitir 2v2, 3v3, 4v4 (pares)
            for team_size in [4, 3, 2]:
                if len(jogadores) >= team_size * 2:
                    team1 = jogadores[:team_size]
                    team2 = jogadores[team_size:team_size*2]
                    break
            else:
                team1 = jogadores[:len(jogadores)//2]
                team2 = jogadores[len(jogadores)//2:len(jogadores)//2*2]

            from utils.emojis import EMOJIS
            # Nomeação: 🎮┃aposta・valor・t1-vs-t2
            def team_names(team):
                return "-".join([guild.get_member(uid).display_name if guild.get_member(uid) else str(uid) for uid in team])
            channel_name = f"{EMOJIS['game']}┃aposta・{valor}・{team_names(team1)}-vs-{team_names(team2)}"

            # Categoria dinâmica
            category_name = "Apostas Rockstar"
            category = discord.utils.get(guild.categories, name=category_name)
            if not category:
                category = await guild.create_category(name=category_name)

            # Permissões: todos jogadores e staff
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            for uid in team1 + team2:
                member = guild.get_member(uid)
                if member:
                    overwrites[member] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            staff_role = discord.utils.get(guild.roles, name="Staff")
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            channel = await guild.create_text_channel(
                name=channel_name,
                overwrites=overwrites,
                category=category
            )

            import json
            confirmations = {str(uid): False for uid in team1 + team2}
            cursor.execute("""
            INSERT INTO matches (guild_id, team1, team2, bet_value, status, channel_id, confirmations)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                guild.id,
                json.dumps(team1),
                json.dumps(team2),
                valor,
                "waiting",
                channel.id,
                json.dumps(confirmations)
            ))

            conn.commit()
            match_id = cursor.lastrowid
            conn.close()

            view = ConfirmView(match_id, team1, team2, valor)
            from utils.embeds import embed_bet
            embed = embed_bet(
                f"{' vs '.join([team_names(team1), team_names(team2)])}\nValor: R${valor}\nClique no botão para confirmar.",
                user=user
            )
            async with channel.typing():
                await asyncio.sleep(1)
                await channel.send(embed=embed, view=view)
            log(f"Partida criada entre {team1} e {team2} por R${valor}")

async def setup(bot):
    await bot.add_cog(QueueCog(bot))