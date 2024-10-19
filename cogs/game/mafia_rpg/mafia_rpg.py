import discord
from discord.ext import commands, tasks
from cogs.game.mafia_rpg.dbhandler import MafiaDBHandler
from cogs.game.mafia_rpg.mafia_config import config as mafia_config
# import random  # Commented out because it's not used

db_handler = MafiaDBHandler()

# Define a view with buttons for player actions
class MafiaActionsView(discord.ui.View):
    def __init__(self, player_id, mafia_game, ctx):
        super().__init__(timeout=None)
        self.player_id = player_id
        self.mafia_game = mafia_game
        self.ctx = ctx

    @discord.ui.button(label="Build", style=discord.ButtonStyle.primary)
    async def build(self, interaction: discord.Interaction):
        """Button to start building/upgrade a facility."""
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        
        build_view = BuildFacilityView(self.player_id, self.mafia_game, self.ctx)
        await interaction.response.send_message("Choose a facility to build/upgrade:", view=build_view, ephemeral=True)

    @discord.ui.button(label="Rob", style=discord.ButtonStyle.success)
    async def rob(self, interaction: discord.Interaction):
        """Button to rob a rival."""
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        await interaction.response.send_message("Who do you want to rob?", ephemeral=True)
        # Use modals for selecting targets or implement dropdowns

    @discord.ui.button(label="View Status", style=discord.ButtonStyle.secondary)
    async def view_status(self, interaction: discord.Interaction):
        """Button to view the player's status."""
        if interaction.user.id != self.player_id:
            await interaction.response.send_message("This is not your game!", ephemeral=True)
            return
        
        await self.mafia_game.display_status(self.ctx, self.player_id)

class BuildFacilityView(discord.ui.View):
    def __init__(self, player_id, mafia_game, ctx):
        super().__init__(timeout=None)
        self.player_id = player_id
        self.mafia_game = mafia_game
        self.ctx = ctx

    @discord.ui.button(label="Upgrade Drug Lab", style=discord.ButtonStyle.primary)
    async def upgrade_drug_lab(self, interaction: discord.Interaction):
        await self.mafia_game.upgrade_facility(self.ctx, self.player_id, "drug_lab")
        await interaction.response.send_message("Upgrading Drug Lab...", ephemeral=True)

    @discord.ui.button(label="Upgrade Weapons Warehouse", style=discord.ButtonStyle.primary)
    async def upgrade_weapons_warehouse(self, interaction: discord.Interaction):
        await self.mafia_game.upgrade_facility(self.ctx, self.player_id, "weapons_warehouse")
        await interaction.response.send_message("Upgrading Weapons Warehouse...", ephemeral=True)

    @discord.ui.button(label="Upgrade Gang Hideout", style=discord.ButtonStyle.primary)
    async def upgrade_gang_hideout(self, interaction: discord.Interaction):
        await self.mafia_game.upgrade_facility(self.ctx, self.player_id, "gang_hideout")
        await interaction.response.send_message("Upgrading Gang Hideout...", ephemeral=True)

class MafiaGame(commands.Cog):
    """Mafia RPG Game with enhanced Discord UI."""
    
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.game_tick.start()  # Start the tick system

    @tasks.loop(minutes=10)
    async def game_tick(self):
        """Every tick (e.g., every 10 minutes), progress the game for all players."""
        for player_id in self.players.keys():
            await self.process_tick(player_id)

    async def process_tick(self, player_id):
        """Handle the game's tick updates for a player."""
        town_info, resources = self.get_player_town_and_resources(player_id)
        drugs, weapons, gang_members = self.update_production(player_id, town_info, resources)
        player = self.bot.get_user(player_id)
        await player.send(f"Tick Update: Drugs: {drugs}, Weapons: {weapons}, Gang Members: {gang_members}")

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

    async def display_status(self, ctx, player_id):
        """Show the current status of the player's town and resources."""
        player_info = db_handler.get_player_info(player_id)
        town_info = db_handler.get_town_info(player_id)
        resources = db_handler.get_resources(player_id)

        status_message = (
            f"🏙️ **{ctx.author.name}'s Town Status** 🏙️\n"
            f"💊 Drug Lab: Level {town_info[1]}\n"
            f"🔫 Weapons Warehouse: Level {town_info[2]}\n"
            f"🏚️ Gang Hideout: Level {town_info[3]}\n"
            f"\n💰 Cash: {player_info[2]}\n"
            f"🌿 Drugs: {resources[0]}\n"
            f"🔫 Weapons: {resources[1]}\n"
            f"🧑‍🤝‍🧑 Gang Members: {resources[2]}"
        )
        await ctx.send(status_message)

    async def upgrade_facility(self, ctx, player_id, facility):
        """Handle upgrading a facility."""
        facility_level = self.get_facility_level(player_id, facility)
        cost = self.calculate_upgrade_cost(facility, facility_level)

        if not self.has_enough_cash(player_id, cost):
            await ctx.send(f"You don't have enough cash to upgrade {facility}. You need {cost} coins.")
            return

        db_handler.update_cash(player_id, -cost)
        db_handler.update_facility(player_id, facility, facility_level + 1)
        await ctx.send(f"Upgraded {facility} to level {facility_level + 1}!")

    def calculate_upgrade_cost(self, facility, facility_level):
        """Calculate the cost for upgrading a facility."""
        facility_config = {
            "drug_lab": {"base_cost": 100, "cost_multiplier": 1.5},
            "weapons_warehouse": {"base_cost": 200, "cost_multiplier": 1.6},
            "gang_hideout": {"base_cost": 150, "cost_multiplier": 1.4},
        }
        return facility_config[facility]["base_cost"] * (facility_config[facility]["cost_multiplier"] ** facility_level)

    def get_facility_level(self, player_id, facility):
        """Retrieve the current level of a facility."""
        facility_index = {"drug_lab": 1, "weapons_warehouse": 2, "gang_hideout": 3}[facility]
        town_info = db_handler.get_town_info(player_id)
        return town_info[facility_index]

    def has_enough_cash(self, player_id, cost):
        """Check if the player has enough cash."""
        player_info = db_handler.get_player_info(player_id)
        return player_info[2] >= cost

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(MafiaGame(bot))
