# cogs/bj_game/__init__.py

from discord.ext import commands

async def setup(bot: commands.Bot):
    """Load the blackjack game cog."""
    await bot.load_extension("cogs.bj_game.blackjack")