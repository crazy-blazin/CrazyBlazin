from discord.ext import commands

async def setup(bot: commands.Bot):
    """Load the Transfer cog."""
    await bot.load_extension("cogs.transfer_commands.transfer")