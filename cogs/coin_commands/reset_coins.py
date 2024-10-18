import discord
from discord.ext import commands
from utils.dbhandler import DataBaseHandler

db_handler = DataBaseHandler()

class ResetCoinsCommand(commands.Cog):
    """Reset a user's coin balance."""

    @commands.command()
    async def reset_coins(self, ctx, member: discord.Member = None):
        """Reset a member's coin balance."""
        if member is None:
            member = ctx.author
        db_handler.reset_coins(user_id=member.id)
        await ctx.send(f"{member.display_name}'s coins have been reset to 0.")

# The setup function to load the cog
async def setup(bot):
    await bot.add_cog(ResetCoinsCommand())
