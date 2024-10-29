import asyncio
import discord
from discord.ext import commands
from loguru import logger
import re
import Levenshtein  # Import the Levenshtein module
from config import config
from utils.signal_handler import setup_signal_handlers

# Initialize bot with intents
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None, case_insensitive=True)

async def load_all_cogs():
    """Load all cogs from different categories."""
    cogs = [
        "cogs.help",
        "cogs.coin_tasks",
        "cogs.coin_commands",
        "cogs.fun_commands",
        "cogs.utility",
        "cogs.game",
        "cogs.transfer_commands",
        "cogs.bj_game"
        ]
    
    for cog in cogs:
        await load_cog(cog)

async def main():
    """Main entry point to start the bot and load cogs."""
    logger.info("Starting the bot and adding cogs...")
    await load_all_cogs()
    
    try:
        await bot.start(config.TOKEN)
    except Exception as e:
        logger.error(f"Failed to start the bot: {e}")

async def load_cog(cog_name: str):
    """Helper function to load a cog and handle errors."""
    try:
        await bot.load_extension(cog_name)
        logger.info(f"Successfully loaded '{cog_name}' cog.")
    except Exception as e:
        logger.error(f"Failed to load '{cog_name}' cog: {e}")

@bot.event
async def on_ready():
    logger.info("Bot started successfully.")

@bot.event
async def on_exit():
    logger.info("Bot is exiting...")
    await bot.close()

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors and run similar commands if found."""
    if isinstance(error, commands.CommandNotFound):
        # Extract the input command and its arguments
        user_input = ctx.message.content
        match = re.match(r'(!\w+)(.*)', user_input)  # Regex to separate command and arguments
        if match:
            command_part = match.group(1).strip('!')  # Extract command without '!'
            args_part = match.group(2).strip()  # Extract arguments
            # Get a list of all available command names
            command_names = [cmd.name for cmd in bot.commands] + [alias for cmd in bot.commands for alias in cmd.aliases]

            # Find the closest command names using Levenshtein distance
            closest_commands = get_closest_commands(command_part, command_names)

            # If there's only one suggestion, attempt to invoke that command
            if len(closest_commands) == 1:
                command_to_invoke = bot.get_command(closest_commands[0])
                if command_to_invoke:  # Check if the command exists
                    try:
                        # Split the arguments into a list (handle numbers and strings)
                        args_list = args_part.split() if args_part else []
                        await ctx.invoke(command_to_invoke, *args_list)
                    except Exception as e:
                        logger.error(f"Failed to invoke command '{closest_commands[0]}': {e}")
            elif closest_commands:
                # Log if there are multiple similar commands found
                logger.warning(f"Multiple commands found that are similar to '{command_part}': {', '.join(closest_commands)}")

def get_closest_commands(command_name, command_names, threshold=2):
    """Get a list of closest command names based on Levenshtein distance."""
    suggestions = []
    for name in command_names:
        distance = Levenshtein.distance(command_name, name)
        if distance <= threshold:
            suggestions.append(name)
    return suggestions

if __name__ == "__main__":
    setup_signal_handlers(bot, on_exit)
    asyncio.run(main())
