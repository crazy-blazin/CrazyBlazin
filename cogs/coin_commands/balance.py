import discord
from discord.ext import commands
from utils.dbhandler import DataBaseHandler

db_handler = DataBaseHandler()

class Balance(commands.Cog):
    """Check user balance."""
    
    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        """Check your coin balance."""
        if member is None:
            member = ctx.author
        result = db_handler.get_coins(user_id=member.id)
        if result is None:
            await ctx.send(f"{member.display_name} has no coins yet.")
        else:
            await ctx.send(f"{member.display_name} has {result[0]} CBC.")

async def setup(bot):
    await bot.add_cog(Balance())
