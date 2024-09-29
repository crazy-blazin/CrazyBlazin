import discord
import asyncio
import random
from datetime import timedelta, datetime
from discord.ext import commands
from beartype import beartype
from loguru import logger
import toml

from utils.dbhandler import DataBaseHandler
from config import config

intents = discord.Intents.default()
intents.voice_states = True  # Track voice states
intents.message_content = True  # To access message content if needed
intents.guilds = True  # To get guild info and members

bot = commands.Bot(command_prefix='!', intents=intents)
db_handler = DataBaseHandler()

# Variable to track whether the multiplier is active
multiplier_active = False


# Function to add coins to a user
@beartype
def add_coins(user_id: int, username: str, amount: int) -> None:
    db_handler.add_coins(user_id=user_id, username=username, amount=amount)


# Background task to give coins to users in voice channels
async def give_coins():
    await bot.wait_until_ready()
    global multiplier_active
    while not bot.is_closed():
        for guild in bot.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if not member.bot:  # Don't give coins to bots
                        coins_to_give = config.PAY_AMOUNT
                        if multiplier_active:  # Apply 2x multiplier
                            coins_to_give *= 2
                        if member.voice.self_stream:  # Check if the member is streaming
                            coins_to_give += config.STREAM_BONUS  # Add bonus coins for streaming
                        db_handler.add_coins(user_id=member.id, username=member.display_name, amount=coins_to_give)
        await asyncio.sleep(config.GRACIOUS_DELAY)


# Background task to handle the random multiplier
async def manage_multiplier():
    await bot.wait_until_ready()
    global multiplier_active

    # Fetch the specific channel by ID
    channel_id = 802307794053234728  # Replace with your channel ID
    channel = bot.get_channel(channel_id)

    while not bot.is_closed():
        # Calculate when the next 24-hour period starts
        next_day = datetime.utcnow() + timedelta(days=1)

        # Choose a random time during the next 24 hours for the multiplier to start
        random_minutes = random.randint(0, config.RANDOM_TIME_WITHIN)  # Random time within 24 hours (in minutes)
        multiplier_start = datetime.utcnow() + timedelta(minutes=random_minutes)

        # Wait until the random start time
        time_to_wait = (multiplier_start - datetime.utcnow()).total_seconds()
        await asyncio.sleep(time_to_wait)

        # Activate the multiplier for 30 minutes
        multiplier_active = True
        logger.info("2x coin multiplier has started!")

        # Send a message to the channel to notify users
        if channel:
            await channel.send("🚀 **2x Coin Multiplier is now active!** Earn double CBC coins for the next 30 minutes!")

        await asyncio.sleep(30 * 60)  # Wait for 30 minutes
        multiplier_active = False
        logger.info("2x coin multiplier has ended!")

        # Send a message to the channel when the multiplier ends
        if channel:
            await channel.send("⏳ **The 2x Coin Multiplier has ended.** Stay tuned for the next random bonus!")

        # Sleep until the start of the next 24-hour period
        time_to_next_day = (next_day - datetime.utcnow()).total_seconds()
        await asyncio.sleep(time_to_next_day)


@bot.event
async def on_ready():
    # Fetch the specific channel by ID
    channel_id = 802307794053234728  # Replace with your channel ID
    channel = bot.get_channel(channel_id)
    # read version with toml
    with open("pyproject.toml", "r") as f:
        data = toml.load(f)
        version = data["tool"]["poetry"]["version"]
    if channel:
        await channel.send(f"🤖 **Bot is online!** Version: {version}")
    logger.info(f"🤖 Bot is online! Version: {version}")

    bot.loop.create_task(give_coins())
    bot.loop.create_task(manage_multiplier())  # Start the multiplier task


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
