import random
import discord
from discord.ext import commands
from loguru import logger
from utils.dbhandler import DataBaseHandler
from config.config import SLOT_PAYOUTS, SLOT_MACHINE_CONFIG, SLOT_WEIGHTS  # Import settings from config.py
import asyncio
from beartype import beartype

db_handler = DataBaseHandler()

class SlotMachineView(discord.ui.View):
    def __init__(self, user, bet, slot_machine_game, ctx, initial_grid=None):
        super().__init__(timeout=60)  # Set a timeout for the buttons
        self.user = user
        self.bet = bet
        self.slot_machine_game = slot_machine_game
        self.ctx = ctx
        self.initial_grid = initial_grid

    @discord.ui.button(label="Spin Again", style=discord.ButtonStyle.primary)
    async def spin_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        # Check if the user still has enough coins to spin again
        user_coins = db_handler.get_coins(user_id=self.user.id)[0]
        if user_coins < self.bet:
            await interaction.response.send_message(f"{self.user.mention}, you don't have enough coins to bet {self.bet}.", ephemeral=True)
            return

        # Deduct the bet amount again and re-spin
        db_handler.add_coins(user_id=self.user.id, username=self.user.name, amount=-int(self.bet))
        logger.info(f"Deducted {self.bet} coins from {self.user.name} for the slot machine bet.")

        await self.slot_machine_game.play_slot(self.ctx, self.bet, interaction)

    @discord.ui.button(label="Change Bet", style=discord.ButtonStyle.secondary)
    async def change_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return

        await interaction.response.send_message("Please type your new bet amount in the chat.", ephemeral=True)

        # Wait for the user to enter the new bet amount
        try:
            msg = await self.slot_machine_game.bot.wait_for(
                "message",
                timeout=30,
                check=lambda message: message.author == self.user and message.channel == self.ctx.channel
            )
            new_bet = int(msg.content)
            await self.slot_machine_game.slot(self.ctx, new_bet)
        except (ValueError, asyncio.TimeoutError):
            await self.ctx.send("Invalid bet amount or time out. Please try again.")

class SlotMachineGame(commands.Cog):
    """Slot Machine game with a customizable grid where users can bet coins and win based on the outcome."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help=f"""Play the slot machine game and try your luck!

        **Usage:**
        `!slot <bet amount>`

        **Example:**
        `!slot 50` - Bet 50 coins on the slot machine.

        **Jackpot Payouts (3 matching symbols on a payline):**
        7️⃣7️⃣7️⃣ : Bet × **{SLOT_PAYOUTS['7️⃣']}**
        ⭐⭐⭐ : Bet × **{SLOT_PAYOUTS['⭐']}**
        🔔🔔🔔 : Bet × **{SLOT_PAYOUTS['🔔']}**
        🍇🍇🍇 : Bet × **{SLOT_PAYOUTS['🍇']}**
        🍉🍉🍉 : Bet × **{SLOT_PAYOUTS['🍉']}**
        🍊🍊🍊 : Bet × **{SLOT_PAYOUTS['🍊']}**
        🍋🍋🍋 : Bet × **{SLOT_PAYOUTS['🍋']}**
        🍒🍒🍒 : Bet × **{SLOT_PAYOUTS['🍒']}**
        """,
        aliases=["slots", "pull"],
        brief="Play the slot machine game and win coins."
    )
    
    async def slot(self, ctx: commands.Context, bet: int | str = None):
        """Allows a user to play the slot machine with a specified bet amount."""
        user = ctx.author
        bet_all: bool = False
        
        if bet is None:
                
            logger.warning(f"{user.name} did not specify a bet amount. Setting bet to 50.")
            bet = 50  # Default bet if no amount is specified
            await ctx.send(f"{user.mention}, No bet specified, betting 50.")
            
            
            
        if isinstance(bet, str):
            if bet.lower() == "all":
                bet_all = True
            else:
                bet = int(bet)
            
        

        
        # Validate bet amount
        if isinstance(bet, int):
            if bet <= 0:
                logger.warning(f"{user.name} attempted to bet an invalid amount: {bet}.")
                await ctx.send("The bet amount must be a positive number.")
                return

        # Check if user has enough coins
        logger.debug(f"{user.name} initiated a slot machine game with a bet of {bet} coins, betting all: {bet_all}.")
        user_coins = db_handler.get_coins(user_id=user.id)[0]
        logger.debug(f"{user.name} has {user_coins} coins.")

        bet = user_coins if bet_all else bet # Bet all coins if the user specifies "all"

        if user_coins < bet:
            logger.warning(f"{user.name} does not have enough coins to bet {bet}.")
            await ctx.send(f"{user.mention}, you don't have enough coins to bet {bet}.")
            return

        # Deduct the bet amount from user's coins
        db_handler.add_coins(user_id=user.id, username=user.name, amount=-bet)
        logger.info(f"Deducted {bet} coins from {user.name} for the slot machine bet.")

        await self.play_slot(ctx, bet)

    async def play_slot(self, ctx: commands.Context, bet: int, interaction=None):
        """Main logic to play the slot game, allowing reuse for spins."""
        user = ctx.author if not interaction else interaction.user

        # Get grid size and spin settings from config
        num_rows = SLOT_MACHINE_CONFIG.get("num_rows", 3)  # Default to 3 rows
        num_cols = SLOT_MACHINE_CONFIG.get("num_cols", 3)  # Default to 3 columns
        num_spins = SLOT_MACHINE_CONFIG.get("num_spins", 5)  # Default to 5 spins

        # Define slot machine emojis
        emojis = list(SLOT_PAYOUTS.keys())
        weights = list(SLOT_WEIGHTS.values())

        # Send initial message with placeholder emojis
        placeholder = "🔳"
        grid_display = [[placeholder for _ in range(num_cols)] for _ in range(num_rows)]
        grid_message = self.format_grid_message(user, grid_display)
        result_message = await (ctx.send(grid_message) if not interaction else interaction.response.edit_message(content=grid_message))

        # Animate the spinning reels
        for _ in range(num_spins):
            # Randomly select emojis for each cell in the grid
            grid_display = [[random.choices(emojis, weights=weights, k=1)[0] for _ in range(num_cols)] for _ in range(num_rows)]
            # Update the message
            grid_message = self.format_grid_message(user, grid_display)
            await result_message.edit(content=grid_message)
            # Wait for a short duration before next spin
            await asyncio.sleep(0.3)

        # Final spin to determine the outcome
        final_grid = grid_display
        final_message_content = self.format_grid_message(user, final_grid, final=True)

        # Determine winnings
        payout, winning_lines = self.calculate_payout(final_grid, bet, num_rows, num_cols)
        if payout > 0:
            # Add winnings to user's coins
            db_handler.add_coins(user_id=user.id, username=user.name, amount=int(payout))
            logger.info(f"Awarded {payout} coins to {user.name} from the slot machine.")
            final_message_content += f"\n\n🎉 You won **{payout}** coins! 🎉\n"
            final_message_content += f"Winning lines: {', '.join(winning_lines)}"
        else:
            final_message_content += "\n\n❌ No winning combinations this time. Better luck next spin!"

        # Update the message with the final result
        await result_message.edit(content=final_message_content)

        # Add buttons to play again or change the bet
        view = SlotMachineView(user, bet, self, ctx, initial_grid=final_grid)
        await result_message.edit(content=final_message_content, view=view)

    def format_grid_message(self, user, grid, final=False):
        """Formats the grid into a message string."""
        title = "🎰 **Slot Machine** 🎰\n\n"
        if not final:
            message = f"{user.mention} is spinning the reels...\n\n"
        else:
            message = f"{user.mention} spun the reels and got:\n\n"

        grid_lines = [' | '.join(row) for row in grid]
        grid_str = '\n'.join(grid_lines)

        return title + message + grid_str

    def calculate_payout(self, grid, bet, num_rows, num_cols):
        """Calculates the payout based on the dynamically generated paylines."""
        payout = 0
        winning_lines = []

        # Generate dynamic paylines
        paylines = self.generate_paylines(num_rows, num_cols)

        # Check each payline for matching symbols
        for line_name, positions in paylines.items():
            symbols = [grid[x][y] for x, y in positions]
            if symbols[0] == symbols[1] == symbols[2]:  # You can adjust this to match variable-length paylines if needed
                symbol = symbols[0]
                line_payout = bet * SLOT_PAYOUTS.get(symbol, 1)
                payout += line_payout
                winning_lines.append(line_name)

        return payout, winning_lines

    def generate_paylines(self, num_rows, num_cols):
        """Generates dynamic paylines based on the grid size."""
        paylines = {}

        # Horizontal lines
        for row in range(num_rows):
            paylines[f"Row {row+1}"] = [(row, col) for col in range(num_cols)]

        # Vertical lines
        for col in range(num_cols):
            paylines[f"Column {col+1}"] = [(row, col) for row in range(num_rows)]

        # Diagonal top-left to bottom-right
        if num_rows == num_cols:
            paylines["Diagonal Top-Left to Bottom-Right"] = [(i, i) for i in range(num_rows)]

            # Diagonal bottom-left to top-right
            paylines["Diagonal Bottom-Left to Top-Right"] = [(i, num_cols - 1 - i) for i in range(num_rows)]

        return paylines
    """
    # Optional: Handle errors globally within the cog
    @slot.error
    async def slot_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid bet amount. Please enter a valid number.")
        else:
            logger.error(f"An error occurred: {error}")
            await ctx.send("An unexpected error occurred. Please try again later.")
    """
# The setup function to load the cog
async def setup(bot):
    await bot.add_cog(SlotMachineGame(bot))
