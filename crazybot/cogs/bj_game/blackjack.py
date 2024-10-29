from dataclasses import dataclass, field
import random
import asyncio

import discord
from discord.ext import commands
from utils.dbhandler import DataBaseHandler

# Define some emojis for suits and card actions
card_emojis = {
    'hearts': '♥️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️',
}
deck_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 10s are for J, Q, K, and 11 for Ace
emoji_hit = "🃏"  # Use an emoji for hit
emoji_stand = "✋"  # Use an emoji for stand

@dataclass
class Blackjack(commands.Cog):
    """Blackjack game with betting feature and emoji reactions."""
    bot: commands.Bot
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
        initial_message = ""
        initial_message += f"{ctx.author.display_name} has placed a bet of {bet} CBC. Let's start!\n"

        # Initialize hands
        player_hand = [self.draw_card(), self.draw_card()]
        dealer_hand = [self.draw_card(), self.draw_card()]

        # Show initial hands
        await self.show_hand(ctx, player_hand, ctx.author.display_name)
        initial_message+=f"Dealer's hand: {dealer_hand[0][0]}{dealer_hand[0][1]} ?"

        # Add reactions for "Hit" and "Stand"
        initial_message +="React with 🃏 to Hit or ✋ to Stand!"
        message = await ctx.send(initial_message)
        print(message)
        await message.add_reaction(emoji_hit)
        await message.add_reaction(emoji_stand)
        
        
        # Ensure the user is not the bot and that they are the one who invoked the command
        def check_reaction(reaction, user):
            print("CTX Author: ", ctx.author)
            print("User:", user)
            return user != self.bot.user and user == ctx.author and str(reaction.emoji) in [emoji_hit, emoji_stand]
            

        # Player turn
        while self.calculate_hand(player_hand) < 21:
            try:
                print("Checking reaction")
                reaction, _ = await ctx.wait_for("reaction_add", timeout=30.0, check=check_reaction)
                print("Reaction: ", reaction)
                if str(reaction.emoji) == emoji_hit:
                    player_hand.append(self.draw_card())
                    await self.show_hand(ctx, player_hand, ctx.author.display_name)
                elif str(reaction.emoji) == emoji_stand:
                    break
            except asyncio.TimeoutError:
                await ctx.send("You took too long! Ending the game.")
                return

        player_total = self.calculate_hand(player_hand)

        # Dealer's turn
        while self.calculate_hand(dealer_hand) < 17:
            dealer_hand.append(self.draw_card())

        dealer_total = self.calculate_hand(dealer_hand)
        await self.show_hand(ctx, dealer_hand, "Dealer")

        # Determine result
        if player_total > 21:
            await ctx.send("Bust! You went over 21 and lost your bet.")
        elif dealer_total > 21 or player_total > dealer_total:
            winnings = bet * 2
            new_balance = self.db_handler.get_coins(user_id=ctx.author.id)[0] + winnings
            self.db_handler.update_coins(user_id=ctx.author.id, amount=new_balance)
            await ctx.send(f"Congratulations! You won {winnings} CBC!")
        elif player_total == dealer_total:
            # Return the bet
            self.db_handler.update_coins(user_id=ctx.author.id, amount=user_balance[0])
            await ctx.send("It's a draw! Your bet has been returned.")
        else:
            await ctx.send("You lost! Better luck next time.")
async def setup(bot):
    await bot.add_cog(Blackjack())
