import os
# Mafia RPG Configuration

# Database settings
MAFIA_DB_NAME = 'mafia_rpg.db'

# Game Settings
TICK_INTERVAL_MINUTES = 10  # How often the game ticks (in minutes)

# Facility Configuration
FACILITY_CONFIG = {
    "drug_lab": {
        "base_cost": 100,
        "cost_multiplier": 1.5,
        "base_production": 10,
    },
    "weapons_warehouse": {
        "base_cost": 200,
        "cost_multiplier": 1.6,
        "base_production": 5,
    },
    "gang_hideout": {
        "base_cost": 150,
        "cost_multiplier": 1.4,
        "base_production": 2,
    },
}

# Robbery and Hit settings
ROBBERY_SETTINGS = {
    "max_percentage": 0.5,  # Max percentage of resources that can be stolen
}

HIT_SETTINGS = {
    "damage_level": 1,  # Number of levels reduced when hit
    "minimum_level": 1,  # Minimum facility level after a hit
}

# Resource Limits
RESOURCE_LIMITS = {
    "max_drugs": 10000,
    "max_weapons": 5000,
    "max_gang_members": 200,
}

# Default starting values for new players
DEFAULT_PLAYER_SETTINGS = {
    "starting_cash": 1000,
    "starting_facilities": {
        "drug_lab": 1,
        "weapons_warehouse": 1,
        "gang_hideout": 1,
    },
    "starting_resources": {
        "drugs": 0,
        "weapons": 0,
        "gang_members": 0,
    },
}

# Leaderboard settings
LEADERBOARD_LIMIT = 5
