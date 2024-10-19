import discord
from discord.ext import commands
from discord.ui import View, Button
from config import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

class AcceptDeclineView(View):
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You accepted!", ephemeral=True)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("You declined!", ephemeral=True)

@bot.command()
async def test(ctx):
    view = AcceptDeclineView()
    await ctx.send("Click a button:", view=view)

bot.run(config.TOKEN)
