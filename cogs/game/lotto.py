import random
import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from loguru import logger
from discord.ext import commands, tasks
from config import config
import asyncio
from dataclasses import dataclass, field
import os

# Keep track of tickets
lotto_tickets = {}

# Create a Lotto View with a Button
class LottoView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Ensures the button doesn't disappear
    
    @discord.ui.button(label="Buy Lotto Ticket", style=discord.ButtonStyle.primary)
    async def buy_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user.id not in lotto_tickets:
            lotto_tickets[user.id] = []
        
        # Generate a random ticket number
        ticket_number = random.randint(1000, 9999)
        lotto_tickets[user.id].append(ticket_number)
        
        await interaction.response.send_message(
            f"🎟️ {user.name} bought a lotto ticket! Ticket number: {ticket_number}", ephemeral=True
        )
        logger.info(f"{user.name} bought a ticket with number {ticket_number}")


### Lotto Roll at 20:00 Daily
@tasks.loop(seconds=5)
async def roll_lotto(ctx):
    if lotto_tickets:
        winning_ticket = random.choice([num for tickets in lotto_tickets.values() for num in tickets])
        winner = None
        for user_id, tickets in lotto_tickets.items():
            if winning_ticket in tickets:
                winner = user_id
                break
        if winner:
            winner_user = await ctx.fetch_user(winner)
            message = f"🏆 The winning ticket is {winning_ticket}! Congratulations {winner_user.name}!"
        else:
            message = "No winners today. Better luck tomorrow!"
        
        # Reset tickets for the next day
        lotto_tickets.clear()
        
        # Send the result to a specific channel (replace CHANNEL_ID with actual channel ID)
        channel = ctx.get_channel(config.CHAT_CHANNEL_ID)  # Make sure to replace with actual channel ID
        await channel.send(message)
        print(f"Lotto rolled. Winning ticket: {winning_ticket}")



@dataclass
class LottoGame(commands.Cog):
    """Lotto game 
        Buy a lotto ticket and win the jackpot!
    """
    bot: commands.Bot = field(default_factory=commands.Bot)

    def __post_init__(self):
        roll_lotto.start()

    @commands.command(
        help="""
        Buy a lotto ticket and win the jackpot! Use `!lotto` to buy a ticket.

        Example usage:
        `!lotto` - Buy a lotto ticket for today's draw!
        """,
        aliases=["lottery", "ticket"],
        brief="Buy a lotto ticket and win the jackpot!"
    )
    async def lotto(self, ctx: commands.Context, bet: int):
        """Buy a lotto ticket and win the jackpot!"""
        view = LottoView(ctx, bet)
        await ctx.send("🎲 Buy your lotto ticket for today's draw!", view=view)


# The setup function to load the cog
async def setup(bot):
    await bot.add_cog(LottoGame(bot))
