import discord
from discord.ext import commands
from discord.ui import Button, View
from loguru import logger
from utils.dbhandler import DataBaseHandler

db_handler = DataBaseHandler()

# Define the button class for Tic-Tac-Toe
class TicTacToeButton(Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=x)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        if view.current_player != interaction.user:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        if self.label != "\u200b":
            await interaction.response.send_message("This position is already taken!", ephemeral=True)
            return

        # Update the button with the current player's symbol (X or O)
        self.label = view.get_symbol_for_player(interaction.user)
        self.style = discord.ButtonStyle.success if view.current_player_symbol == "X" else discord.ButtonStyle.danger
        self.disabled = True

        # Update the game state
        view.board[self.x][self.y] = view.current_player_symbol

        if view.check_winner():
            await interaction.response.edit_message(content=f"Game over! {interaction.user.mention} won!", view=view)
            view.disable_all_buttons()
            view.award_winner(interaction.user)
        elif view.is_tie():
            await interaction.response.edit_message(content="It's a tie!", view=view)
            view.disable_all_buttons()
            view.refund_bets()
        else:
            # Switch turns
            view.switch_turns()
            await interaction.response.edit_message(content=f"It's {view.current_player.mention}'s turn!", view=view)


# Define the view class for Tic-Tac-Toe
class TicTacToeView(View):
    def __init__(self, player_x: discord.User, player_o: discord.User, bet_amount: int):
        super().__init__()
        self.current_player = player_x
        self.player_x = player_x
        self.player_o = player_o
        self.current_player_symbol = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.bet_amount = bet_amount

        # Deduct coins from both players
        db_handler.add_coins(user_id=self.player_x.id, username=self.player_x.name, amount=-self.bet_amount)
        db_handler.add_coins(user_id=self.player_o.id, username=self.player_o.name, amount=-self.bet_amount)

        # Add buttons to the view (3x3 grid)
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def get_symbol_for_player(self, player: discord.User) -> str:
        """Return the symbol (X or O) for the current player."""
        return "X" if player == self.player_x else "O"

    def switch_turns(self):
        """Switch the turn between the two players."""
        self.current_player = self.player_o if self.current_player == self.player_x else self.player_x
        self.current_player_symbol = "X" if self.current_player_symbol == "O" else "O"

    def check_winner(self) -> bool:
        """Check if there is a winner."""
        # Rows, columns, and diagonals
        lines = (
            self.board,  # rows
            zip(*self.board),  # columns
            [[self.board[i][i] for i in range(3)], [self.board[i][2 - i] for i in range(3)]],  # diagonals
        )
        for line in lines:
            for triplet in line:
                if triplet[0] == triplet[1] == triplet[2] != "":
                    return True
        return False

    def is_tie(self) -> bool:
        """Check if the game is a tie."""
        return all(cell != "" for row in self.board for cell in row)

    def disable_all_buttons(self):
        """Disable all buttons after the game ends."""
        for child in self.children:
            child.disabled = True
        self.stop()

    def award_winner(self, winner: discord.User):
        """Award the total bet amount to the winner."""
        total_bet = self.bet_amount * 2
        db_handler.add_coins(user_id=winner.id, username=winner.name, amount=total_bet)
        logger.info(f"Awarded {total_bet} coins to {winner.name}")

    def refund_bets(self):
        """Refund the bet amount to both players in case of a tie."""
        db_handler.add_coins(user_id=self.player_x.id, username=self.player_x.name, amount=self.bet_amount)
        db_handler.add_coins(user_id=self.player_o.id, username=self.player_o.name, amount=self.bet_amount)
        logger.info(f"Refunded {self.bet_amount} coins to {self.player_x.name} and {self.player_o.name}")


# Define the command for starting the Tic-Tac-Toe game
class TicTacToeGame(commands.Cog):
    """Tic-Tac-Toe game with betting between two players."""

    @commands.command()
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member, bet: int):
        """Start a Tic-Tac-Toe game between the author and the opponent with a bet."""
        if opponent.bot:
            await ctx.send("You can't play against a bot!")
            return

        # Validate bet amount
        if bet <= 0:
            await ctx.send("The bet amount must be a positive number.")
            return

        # Check if both players have enough coins
        author_coins = db_handler.get_coins(user_id=ctx.author.id)[0]
        opponent_coins = db_handler.get_coins(user_id=opponent.id)[0]

        if author_coins < bet:
            await ctx.send(f"{ctx.author.mention}, you don't have enough coins to bet {bet}.")
            return
        if opponent_coins < bet:
            await ctx.send(f"{opponent.mention} doesn't have enough coins to bet {bet}.")
            return

        # Start the game with the bet
        view = TicTacToeView(ctx.author, opponent, bet)
        await ctx.send(f"Tic-Tac-Toe: {ctx.author.mention} vs {opponent.mention}\n{ctx.author.mention}'s turn (X)\nBet: {bet} coins each", view=view)

# The setup function to load the cog
async def setup(bot):
    await bot.add_cog(TicTacToeGame())
