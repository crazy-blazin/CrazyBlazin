import random
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from loguru import logger
from config import config
from dataclasses import dataclass, field
from utils.dbhandler import DataBaseHandler
from datetime import datetime, timedelta, time, timezone

# Initialize database handler
db_handler = DataBaseHandler()

# Keep track of tickets
lotto_tickets = {}


# Create a Lotto View with a Button
class LottoView(View):
    def __init__(self, msg):
        super().__init__(timeout=None)  # Ensures the button doesn't disappear
        self.msg = msg

    @discord.ui.button(label="Buy Lotto Ticket", style=discord.ButtonStyle.primary)
    async def buy_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        user_id = user.id

        # Check if user has enough coins (1 coin per ticket)
        user_coins = db_handler.get_coins(user_id=user_id)[0]
        if user_coins < 1:
            await interaction.response.send_message("You don't have enough coins to buy a ticket.", ephemeral=True)
            return

        # Deduct 1 coin for buying a ticket
        db_handler.add_coins(user_id=user_id, username=user.name, amount=-1)

        if user_id not in lotto_tickets:
            lotto_tickets[user_id] = []

        # Generate a random ticket number
        ticket_number = random.randint(1000, 9999)
        lotto_tickets[user_id].append(ticket_number)

        # Update the message to show the current draw info
        tickets_info = "\n".join(
            [f"{interaction.guild.get_member(uid).name}: {len(tickets)} tickets" for uid, tickets in lotto_tickets.items()]
        )
        await self.msg.edit(content=f"🎲 Buy your lotto ticket for today's draw!\n\n**Current Draw:**\n{tickets_info}")

        await interaction.response.send_message(
            f"🎟️ {user.name} bought a lotto ticket! Ticket number: {ticket_number}", ephemeral=True
        )
        logger.info(f"{user.name} bought a ticket with number {ticket_number}")

### Lotto Roll Task
@tasks.loop(seconds=5)#(time=time(20, 00, tzinfo=timezone(timedelta(hours=2))))
async def roll_lotto(ctx):
    if lotto_tickets:
        winning_ticket = random.randint(1000, 9999)
        winner = None
        for user_id, tickets in lotto_tickets.items():
            if winning_ticket in tickets:
                winner = user_id
                break

        if winner:
            winner_user = await ctx.fetch_user(winner)
            reward = config.LOTTO_REWARD_AMOUNT  # Get reward from config
            db_handler.add_coins(user_id=winner, username=winner_user.name, amount=reward)
            message = f"🏆 The winning ticket is {winning_ticket}! Congratulations {winner_user.name}! You've won {reward} coins!"
        else:
            message = f"No winners today. Better luck tomorrow! Winning ticket #: 🎟️ {winning_ticket}"

        # Reset tickets for the next day
        lotto_tickets.clear()

        # Send the result to a specific channel (replace CHANNEL_ID with actual channel ID)
        channel = ctx.get_channel(config.CHAT_CHANNEL_ID)
        if channel:
            await channel.send(message)
        else:
            logger.error("Channel not found. Check your CHANNEL_ID.")
        
        logger.info(f"Lotto rolled. Winning ticket: {winning_ticket}")
    else:
        logger.info("No tickets were bought today.")

@dataclass
class LottoGame(commands.Cog):
    """Lotto game 
    Buy a lotto ticket and win the jackpot!
    """
    bot: commands.Bot = field(default_factory=commands.Bot)

    def __post_init__(self):
        # Start the lotto roll loop when the cog is loaded
        logger.info("Starting Lotto Roll Task...")
        roll_lotto.start(ctx=self.bot)

    @commands.command(
        help="""Buy a lotto ticket and win the jackpot! Use `!lotto` to buy a ticket.""",
        aliases=["lottery", "ticket"],
        brief="Buy a lotto ticket and win the jackpot!"
    )
    async def lotto(self, ctx: commands.Context):
        """Buy a lotto ticket and win the jackpot!"""
        view = LottoView(msg=await ctx.send("🎲 Buy your lotto ticket for today's draw!"))
        await view.msg.edit(view=view)  # Set the view for the existing message
        logger.info("Lotto command used.")

# The setup function to load the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(LottoGame(bot))
