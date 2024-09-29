import discord
import asyncio
from discord.ext import commands
from utils.dbhandler import DataBaseHandler
from config import config

intents = discord.Intents.default()
intents.voice_states = True  # Track voice states
intents.message_content = True  # To access message content if needed
intents.guilds = True  # To get guild info and members

bot = commands.Bot(command_prefix='!', intents=intents)
db_handler = DataBaseHandler()


# Function to add coins to a user
def add_coins(user_id, username, amount):
    db_handler.add_coins(user_id=user_id, username=username, amount=amount)


# Background task to give coins to users in voice channels
async def give_coins():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if not member.bot:  # Don't give coins to bots
                        db_handler.add_coins(user_id=member.id, username=member.display_name, amount=config.PAY_AMOUNT)
        await asyncio.sleep(config.GRACIOUS_DELAY)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(give_coins())


@bot.command()
async def balance(ctx, member: discord.Member = None):
    """Check your coin balance."""
    if member is None:
        member = ctx.author
    result = db_handler.get_coins(user_id=member.id)
    if result is None:
        await ctx.send(f"{member.display_name} has no coins yet.")
    else:
        await ctx.send(f"{member.display_name} has {result[0]} CBC coins.")


@bot.command()
async def reset_coins(ctx, member: discord.Member = None):
    """Reset a member's coin balance."""
    if member is None:
        member = ctx.author
    db_handler.reset_coins(user_id=member.id)
    await ctx.send(f"{member.display_name}'s coins have been reset to 0.")

bot.run(config.TOKEN)
