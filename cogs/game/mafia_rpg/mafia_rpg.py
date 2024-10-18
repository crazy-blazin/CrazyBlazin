import discord
from discord.ext import commands, tasks
from utils.dbhandler import MafiaDBHandler
import random

db_handler = MafiaDBHandler()

class MafiaGame(commands.Cog):
    """Mafia RPG Game where players build a criminal empire."""

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.game_tick.start()  # Start the tick system

    @tasks.loop(minutes=3)
    async def game_tick(self):
        """Every tick (e.g., every 10 minutes), progress the game for all players."""
        for player_id in self.players.keys():
            await self.process_tick(player_id)

    async def process_tick(self, player_id):
        """Handle the game's tick updates for a player."""
        try:
            town_info, resources = self.get_player_town_and_resources(player_id)
            drugs, weapons, gang_members = self.update_production(player_id, town_info, resources)
            await self.notify_player(player_id, drugs, weapons, gang_members)
        except Exception as e:
            print(f"Error processing tick for player {player_id}: {e}")

    def get_player_town_and_resources(self, player_id):
        """Retrieve both town and resource data for a player."""
        town_info = db_handler.get_town_info(player_id)
        resources = db_handler.get_resources(player_id)
        return town_info, resources

    def update_production(self, player_id, town_info, resources):
        """Update the production of resources based on facility levels."""
        drug_lab_level = town_info[1]
        weapons_level = town_info[2]
        gang_level = town_info[3]

        drugs = resources[0] + drug_lab_level * 10
        weapons = resources[1] + weapons_level * 5
        gang_members = resources[2] + gang_level * 2

        db_handler.update_resource(player_id, "drugs", drugs)
        db_handler.update_resource(player_id, "weapons", weapons)
        db_handler.update_resource(player_id, "gang_members", gang_members)

        return drugs, weapons, gang_members

    async def notify_player(self, player_id, drugs, weapons, gang_members):
        """Notify the player of updated resources."""
        player = self.bot.get_user(player_id)
        await player.send(f"Tick Update: Drugs: {drugs}, Weapons: {weapons}, Gang Members: {gang_members}")

    @commands.command()
    async def build(self, ctx, facility: str):
        """Build or upgrade a facility in your town."""
        player_id = ctx.author.id

        facility_info = self.get_facility_info(facility)
        if not facility_info:
            await ctx.send("Invalid facility name. Choose from: drug_lab, weapons_warehouse, gang_hideout.")
            return

        facility_level = self.get_facility_level(player_id, facility)
        cost = self.calculate_upgrade_cost(facility_info, facility_level)

        if not self.has_enough_cash(player_id, cost):
            await ctx.send(f"You don't have enough cash to upgrade {facility}. You need {cost} coins.")
            return

        self.perform_upgrade(player_id, facility, facility_level, cost)
        await ctx.send(f"Upgraded {facility} to level {facility_level + 1}!")

    def get_facility_info(self, facility):
        """Retrieve the facility information from config."""
        facilities = {
            "drug_lab": {"emoji": "💊", "base_cost": 100, "cost_multiplier": 1.5},
            "weapons_warehouse": {"emoji": "🔫", "base_cost": 200, "cost_multiplier": 1.6},
            "gang_hideout": {"emoji": "🏚️", "base_cost": 150, "cost_multiplier": 1.4},
        }
        return facilities.get(facility)

    def calculate_upgrade_cost(self, facility_info, facility_level):
        """Calculate the cost for upgrading a facility."""
        return facility_info["base_cost"] * (facility_info["cost_multiplier"] ** facility_level)

    def get_facility_level(self, player_id, facility):
        """Retrieve the current level of a facility."""
        facility_index = {"drug_lab": 1, "weapons_warehouse": 2, "gang_hideout": 3}[facility]
        town_info = db_handler.get_town_info(player_id)
        return town_info[facility_index]

    def has_enough_cash(self, player_id, cost):
        """Check if the player has enough cash."""
        player_info = db_handler.get_player_info(player_id)
        return player_info[2] >= cost

    def perform_upgrade(self, player_id, facility, current_level, cost):
        """Deduct cash and upgrade the facility."""
        db_handler.update_cash(player_id, -cost)
        db_handler.update_facility(player_id, facility, current_level + 1)

    @commands.command()
    async def rob(self, ctx, target: discord.Member):
        """Plan a robbery on a rival's town."""
        attacker_id = ctx.author.id
        defender_id = target.id

        if not self.can_rob(attacker_id, defender_id):
            await ctx.send("This player has no resources to rob.")
            return

        loot = self.perform_robbery(attacker_id, defender_id)
        await ctx.send(f"Robbery successful! {ctx.author.mention} stole: {loot} from {target.mention}!")

    def can_rob(self, attacker_id, defender_id):
        """Check if a player can rob another player."""
        defender_resources = db_handler.get_resources(defender_id)
        return sum(defender_resources) > 0

    def perform_robbery(self, attacker_id, defender_id):
        """Handle the robbery logic and resource transfer."""
        defender_resources = db_handler.get_resources(defender_id)
        loot = {
            "drugs": random.randint(0, defender_resources[0] // 2),
            "weapons": random.randint(0, defender_resources[1] // 2),
            "gang_members": random.randint(0, defender_resources[2] // 2),
        }

        self.update_player_resources(attacker_id, loot, add=True)
        self.update_player_resources(defender_id, loot, add=False)
        return loot

    def update_player_resources(self, player_id, loot, add=True):
        """Update player resources based on the loot."""
        resources = db_handler.get_resources(player_id)
        factor = 1 if add else -1

        new_drugs = resources[0] + factor * loot["drugs"]
        new_weapons = resources[1] + factor * loot["weapons"]
        new_gang_members = resources[2] + factor * loot["gang_members"]

        db_handler.update_resource(player_id, "drugs", new_drugs)
        db_handler.update_resource(player_id, "weapons", new_weapons)
        db_handler.update_resource(player_id, "gang_members", new_gang_members)

    # Similar refactoring for the hit, grow, and other commands...

# The setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(MafiaGame(bot))
