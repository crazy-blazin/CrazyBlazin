from discord.ext import commands

async def setup(bot: commands.Bot):
    """Load the Tic-Tac-Toe game cog."""
    await bot.load_extension("cogs.game.tic_tac_toe")
