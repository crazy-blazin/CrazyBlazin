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

# Track the last time someone was awarded for being the first to join any voice channel
last_awarded_time = None

# Function to add coins to a user
@beartype
def add_coins(user_id: int, username: str, amount: int) -> None:
    db_handler.add_coins(user_id=user_id, username=username, amount=amount)


@bot.event
async def on_voice_state_update(member, before, after):
    global last_awarded_time

    # Check if the member has joined a voice channel
    if after.channel is not None and before.channel != after.channel:
        now = datetime.utcnow()
        # If there hasn't been a first joiner in the past 24 hours
        if last_awarded_time is None or now - last_awarded_time >= timedelta(days=config.FIRST_IN_CHANNEL_TIMER_DAYS):
            # Award coins to the first joiner in 24 hours
            first_join_reward = config.FIRST_IN_CHANNEL_REWARD_COINS  # Adjust the reward amount as you wish
            db_handler.add_coins(user_id=member.id, username=member.display_name, amount=first_join_reward)

            # Send a message to the specific text channel
            announcement_channel = bot.get_channel(802307794053234728)
            if announcement_channel:
                await announcement_channel.send(f"🎉 {member.display_name} is the first to join a voice channel in the past 24 hours and earns {first_join_reward} CBC coins!")

            # Update the last awarded time
            last_awarded_time = now


# Background task to give coins to users in voice channels
async def give_coins():
    await bot.wait_until_ready()
    global multiplier_active

    while not bot.is_closed():
        for guild in bot.guilds:
            # Fetch leaderboard from the database (this is an example, adjust for your system)
            for vc in guild.voice_channels:
                for member in vc.members:
                    if not member.bot:  # Skip bots
                        coins_to_give = config.PAY_AMOUNT

                        # Apply 2x multiplier if it's active
                        if multiplier_active:
                            coins_to_give *= config.EVENT_MULTIPLIER

                        # Add bonus coins if the member is streaming
                        if member.voice.self_stream:
                            coins_to_give += config.STREAM_BONUS

                        # Give coins to the member
                        db_handler.add_coins(user_id=member.id, username=member.display_name, amount=coins_to_give)

        # Wait for the next cycle
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
        logger.info(f"{config.EVENT_MULTIPLIER}x coin multiplier has started!")

        # Send a message to the channel to notify users
        if channel:
            await channel.send(f"🚀 **{config.EVENT_MULTIPLIER}x Coin Multiplier is now active!** Earn double CBC coins for the next {config.BONUS_TIMER_MINUTES} minutes!")

        await asyncio.sleep(config.BONUS_TIMER_MINUTES)
        multiplier_active = False
        logger.info(f"{config.EVENT_MULTIPLIER}x coin multiplier has ended!")

        # Send a message to the channel when the multiplier ends
        if channel:
            await channel.send(f"⏳ **The {config.EVENT_MULTIPLIER}x Coin Multiplier has ended.** Stay tuned for the next random bonus!")

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
        # await channel.send(f"🤖 **Bot is online!** Version: {version}")
        pass
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


@bot.command()
async def leaderboard(ctx):
    """Display the top 10 users with the most coins."""
    top_users = db_handler.get_top_users(limit=10)  # Assumes db_handler has a method for this
    if not top_users:
        await ctx.send("No one has earned any coins yet.")
        return

    leaderboard_text = "**Top Coin Leaders:**\n"
    position = 1
    for _, username, coins in top_users:
        if position == 1:
            leaderboard_text += f"🥇 **{username}**: {coins} coins\n"
        elif position == 2:
            leaderboard_text += f"🥈 **{username}**: {coins} coins\n"
        elif position == 3:
            leaderboard_text += f"🥉 **{username}**: {coins} coins\n"
        else:
            leaderboard_text += f"{position}. **{username}**: {coins} coins\n"
        position += 1

    embed = discord.Embed(title="Leaderboard", description=leaderboard_text, color=0x00ff00)
    await ctx.send(embed=embed)



bot.run(config.TOKEN)
