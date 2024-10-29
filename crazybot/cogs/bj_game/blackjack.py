import discord
from discord.ext import commands
from discord.ui import Button, View
from dataclasses import dataclass, field
import random
import asyncio

from utils.dbhandler import DataBaseHandler

# Define some emojis for suits and card actions
card_emojis = {
    'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️',
}
deck_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 10s are for J, Q, K, and 11 for Ace

# Define emojis for buttons
emoji_hit = "🃏"  # Use an emoji for hit
emoji_stand = "✋"  # Use an emoji for stand

@dataclass
class Blackjack(commands.Cog):
    """Blackjack game with betting feature and emoji reactions."""
    db_handler: DataBaseHandler = field(default_factory=DataBaseHandler)

    def draw_card(self) -> tuple:
        """Draw a card from the deck and return its value and suit."""
        value = random.choice(deck_values)
        suit = random.choice(list(card_emojis.values()))
        return value, suit

    async def show_hand(self, ctx, hand, name):
        """Display a player's hand in the chat with emojis."""
        cards = ' '.join(f"{value}{suit}" for value, suit in hand)
        await ctx.send(f"{name}'s hand: {cards} (Total: {self.calculate_hand(hand)})")

    def calculate_hand(self, hand):
        """Calculate the total value of a hand, adjusting for aces."""
        total = sum(card[0] for card in hand)
        aces = sum(1 for card in hand if card[0] == 11)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    @commands.command(
        help="Start a blackjack game with a bet. Example: `!blackjack <bet>`",
        brief="Play a game of blackjack with a bet."
    )
    async def blackjack(self, ctx, bet: int):
        """Play a game of blackjack with betting and emoji reactions."""
        if bet is None:
            bet = 20
        if bet <= 0:
            await ctx.send("Please place a valid bet greater than 0.")
            return

        user_balance = self.db_handler.get_coins(user_id=ctx.author.id)
        if user_balance is None or user_balance[0] < bet:
            await ctx.send("You don't have enough coins to place this bet!")
            return

        # Deduct the bet amount from the user’s balance
        self.db_handler.update_coins(user_id=ctx.author.id, amount=user_balance[0] - bet)

        # Initialize hands
        player_hand = [self.draw_card(), self.draw_card()]
        dealer_hand = [self.draw_card(), self.draw_card()]

        # Show initial hands
        await self.show_hand(ctx, player_hand, ctx.author.display_name)
        await self.show_hand(ctx, dealer_hand, "Dealer")

        # Create and send the view with buttons
        view = BlackjackView(self, ctx, player_hand, dealer_hand, bet)
        await ctx.send("React with the buttons below to play!", view=view)

class BlackjackButton(Button):
    def __init__(self, label, style, callback, emoji=None):
        super().__init__(label=label, style=style, emoji=emoji)
        self.callback = callback

class BlackjackView(View):
    def __init__(self, cog, ctx, player_hand, dealer_hand, bet):
        super().__init__(timeout=None)
        self.cog = cog
        self.ctx = ctx
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.bet = bet

        self.add_item(BlackjackButton(emoji_hit + " Hit", discord.ButtonStyle.primary, self.hit))
        self.add_item(BlackjackButton(emoji_stand + " Stand", discord.ButtonStyle.secondary, self.stand))

    async def hit(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction
        self.player_hand.append(self.cog.draw_card())
        await self.cog.show_hand(self.ctx, self.player_hand, self.ctx.author.display_name)

        if self.cog.calculate_hand(self.player_hand) > 21:
            await interaction.followup.send("Bust! You went over 21 and lost your bet.")
            self.disable_all_items()
            await interaction.message.edit(view=self)
            self.stop()
        elif self.cog.calculate_hand(self.player_hand) == 21:
            await interaction.followup.send("Blackjack! You won 1.5x your bet.")
            winnings = self.bet * 1.5
            new_balance = self.cog.db_handler.get_coins(user_id=self.ctx.author.id)[0] + winnings
            self.cog.db_handler.update_coins(user_id=self.ctx.author.id, amount=new_balance)
            self.disable_all_items()
            await interaction.message.edit(view=self)
            self.stop()

    async def stand(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Acknowledge the interaction
        while self.cog.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.cog.draw_card())
        await self.cog.show_hand(self.ctx, self.dealer_hand, "Dealer")

        player_total = self.cog.calculate_hand(self.player_hand)
        dealer_total = self.cog.calculate_hand(self.dealer_hand)


        if player_total > 21:
            await interaction.followup.send("Bust! You went over 21 and lost your bet.")
        elif dealer_total > 21 or player_total > dealer_total:
            winnings = self.bet * 2
            new_balance = self.cog.db_handler.get_coins(user_id=self.ctx.author.id)[0] + winnings
            self.cog.db_handler.update_coins(user_id=self.ctx.author.id, amount=new_balance)
            await interaction.followup.send(f"Congratulations! You won {winnings} CBC!")
        elif player_total == dealer_total:
            self.cog.db_handler.update_coins(user_id=self.ctx.author.id, amount=self.bet)
            await interaction.followup.send("It's a draw! Your bet has been returned.")
        else:
            await interaction.followup.send("You lost! Better luck next time.")
        
        self.disable_all_items()
        await interaction.message.edit(view=self)
        self.stop()

# The setup function to load the cog
async def setup(bot):
    await bot.add_cog(Blackjack())