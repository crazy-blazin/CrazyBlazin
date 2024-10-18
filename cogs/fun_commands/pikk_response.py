from dataclasses import dataclass

from discord.ext import commands


@dataclass
class PikkResponse(commands.Cog):
    """Respond to 'Pikk' with 'Hello beautiful!'"""

    @commands.Cog.listener()
    async def on_message(self, message):
        if "pikk" in message.content.lower():
            await message.channel.send("Hello beautiful!")

async def setup(bot):
    await bot.add_cog(PikkResponse())
