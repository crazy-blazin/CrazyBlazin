from discord.ext import commands
import time

class Uptime(commands.Cog):
    """Check how long the bot has been running."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def uptime(self, ctx):
        """Shows the bot's uptime."""
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Uptime: {hours}h {minutes}m {seconds}s")

async def setup(bot):
    await bot.add_cog(Uptime(bot))
