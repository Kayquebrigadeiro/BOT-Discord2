import discord
import asyncio
from database import connect
from services.payment_service import calculate_tax, get_active_mediator


import json

class ConfirmView(discord.ui.View):
    def __init__(self, match_id, team1, team2, bet_value, timeout=60):
        super().__init__(timeout=timeout)
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.bet_value = bet_value

    @discord.ui.button(label="Confirmar Aposta", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from utils.embeds import embed_error, embed_success, embed_bet
        user_id = interaction.user.id

        if user_id not in self.team1 + self.team2:
            await interaction.response.send_message(
                embed=embed_error("Você não participa desta aposta.", user=interaction.user),
                ephemeral=True
            )
            return

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT confirmations FROM matches WHERE id=?", (self.match_id,))
        confirmations = json.loads(cursor.fetchone()[0])
        confirmations[str(user_id)] = True
        cursor.execute("UPDATE matches SET confirmations=? WHERE id=?", (json.dumps(confirmations), self.match_id))
        conn.commit()

        # Se todos confirmaram
        if all(confirmations.get(str(uid), False) for uid in self.team1 + self.team2):
            cursor.execute("UPDATE matches SET status='confirmed' WHERE id=?", (self.match_id,))
            conn.commit()

            tax = calculate_tax(interaction.guild.id, self.bet_value)
            mediator = get_active_mediator(interaction.guild.id)

            if not mediator:
                await interaction.channel.send(embed=embed_error("Nenhum mediador ativo configurado."))
                return

            name, pix_key = mediator
            total = self.bet_value + tax

            embed = embed_bet(
                f"✅ Todos confirmaram!\n\n"
                f"💳 **PIX:** `{pix_key}`\n"
                f"👤 **Titular:** `{name}`\n"
                f"💰 **Valor:** `R${self.bet_value}`\n"
                f"🧾 **Taxa:** `R${tax}`\n"
                f"💵 **Total:** `R${total}`",
                user=interaction.user
            )
            async with interaction.channel.typing():
                await asyncio.sleep(1)
                await interaction.channel.send(embed=embed)

            await asyncio.sleep(30)
            await interaction.channel.delete()

        else:
            await interaction.response.send_message(
                embed=embed_success("Confirmação registrada. Aguarde os outros jogadores.", user=interaction.user),
                ephemeral=True
            )

        conn.close()

    async def on_timeout(self):
        from utils.embeds import embed_error
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE matches SET status='cancelled' WHERE id=?", (self.match_id,))
        conn.commit()
        conn.close()
        # Optionally notify users in the channel if it still exists
        try:
            await self.message.edit(embed=embed_error("Tempo esgotado! A aposta foi cancelada."))
        except Exception:
            pass