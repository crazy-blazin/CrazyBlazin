import os
from typing import Dict

# Security settings
TOKEN = os.getenv('CRAZY_TOKEN')

# Payment settings
PAY_AMOUNT = 1
STREAM_BONUS = 5
FIRST_IN_CHANNEL_REWARD_COINS = 500
FIRST_IN_CHANNEL_TIMER_DAYS = 1
BONUS_TIMER_MINUTES = 30
PAY_INTERVAL = 5

# Database settings

DB_NAME =  'C:/Users/Moh/Documents/GitHub/CrazyBlazin/data/coins.db'

# Multiplier settings
RANDOM_TIME_WITHIN = 23 * 60 + 30 # 23 hours and 30 minutes
EVENT_MULTIPLIER = 5
SPECIAL_EVENT_MULTIPLIER = 3

# Grace
GRACIOUS_DELAY = 5

# chat
CHAT_CHANNEL_ID = 803982821923356773

##---------------------- Lotto settings ----------------------##
LOTTO_TICKET_PRICE = 150
LOTTO_BASELINE = 50000

SLOT_WEIGHTS: Dict[str, float] = {
    "7️⃣": 0.0002,   # Very rare symbol (high payout)
    "⭐": 0.0003,     # Rare symbol (reduced frequency)
    "🔔": 0.002,      # Mid-range symbol (reduced frequency)
    "🍇": 0.075,      # Common fruit symbol (medium payout)
    "🍉": 0.10,       # Common fruit symbol (medium payout)
    "🍊": 0.15,       # Common fruit symbol (low payout, higher chance)
    "🍋": 0.25,       # Common fruit symbol (low payout, higher chance)
    "🍒": 0.40        # Most common symbol (lowest payout)
}

# Define the payouts for each symbol
SLOT_PAYOUTS: Dict[str, int] = {
    "7️⃣": 75.0,    # Reduced high payout
    "⭐": 50.0,      # Reduced medium payout
    "🔔": 25.0,     # Reduced medium payout
    "🍇": 8.0,      # Lowered medium payout
    "🍉": 4.0,      # Lowered small payout
    "🍊": 2.0,      # Lowered small payout
    "🍋": 1.5,      # Lowered small payout
    "🍒": 1.2       # Lowest payout

}


# Add settings for the grid size
SLOT_MACHINE_CONFIG: Dict[str, int] = {
    "num_rows": 3,
    "num_cols": 3,  # You can change this to make it a larger or smaller grid
    "num_spins": 4  # Number of times the reels will spin
}
##---------------------------------------------------------------##
