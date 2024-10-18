from discord.ext import tasks, commands
from utils.dbhandler import DataBaseHandler
from config import config

db_handler = DataBaseHandler()

class GiveCoinsTask(commands.Cog):
    """Task to give coins to users in voice channels."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.give_coins.start()

    @tasks.loop(minutes=config.GRACIOUS_DELAY / 60)
    async def give_coins(self):
        """Give coins to users in active voice channels."""
        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if not member.bot:  # Skip bots
                        coins_to_give = config.PAY_AMOUNT
                        db_handler.add_coins(user_id=member.id, username=member.display_name, amount=coins_to_give)

    @give_coins.before_loop
    async def before_give_coins(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(GiveCoinsTask(bot))
