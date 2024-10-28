from dataclasses import dataclass, field

import discord
from discord.ext import commands

from utils.dbhandler import DataBaseHandler

@dataclass
class Transfer(commands.Cog):
    """Cog for transferring coins between users."""
    db_handler: DataBaseHandler = field(default_factory=DataBaseHandler)

    @commands.command(
        help="""Transfer coins to another user. 
                Usage: `!transfer @user amount`.""",
        aliases=["send", "give"],
        brief="Transfer coins to another user."
    )
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer coins from the command author to another user."""
        sender_id = ctx.author.id
        receiver_id = member.id
        
        # Check for self-transfer attempt
        if sender_id == receiver_id:
            await ctx.send("You can't transfer coins to yourself.")
            return

        # Validate the amount is positive
        if amount <= 0:
            await ctx.send("Please enter a positive amount to transfer.")
            return

        # Attempt to transfer coins using db_handler
        success = self.db_handler.transfer_coins(sender_id, receiver_id, amount)

        # Send transfer result message
        if success:
            await ctx.send(f"Successfully transferred {amount} CBC to {member.display_name}.")
        else:
            await ctx.send("Transfer failed. You may not have enough coins.")

# Ensure this setup function is in the transfer.py file
async def setup(bot: commands.Bot):
    await bot.add_cog(Transfer())