import os

# Security settings
TOKEN = os.getenv('CRAZY_TOKEN')

# Payment settings
PAY_AMOUNT = 1
STREAM_BONUS = 1
FIRST_IN_CHANNEL_REWARD_COINS = 300
FIRST_IN_CHANNEL_TIMER_DAYS = 1

# Database settings
DB_NAME = '/data/coins.db'

# Multiplier settings
RANDOM_TIME_WITHIN = 23 * 60 + 30 # 23 hours and 30 minutes


# Grace
GRACIOUS_DELAY = 5
