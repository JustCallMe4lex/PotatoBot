import json
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

class ReportModal(discord.ui.Modal, title="User Report Form"):
    user_name = discord.ui.TextInput(
        label="User's Discord Name",
        placeholder="e.g. DeezNuts#1234",
        required=True,
        max_length=100,
        style=discord.TextStyle.short
    )
    user_id = discord.ui.TextInput(
        label="User's Discord ID",
        placeholder="Make sure developer mode is on to get a User ID.",
        required=True,
        min_length=18,
        max_length=18,
        style=discord.TextStyle.short
    )
    description = discord.ui.TextInput(
        label="What did they do?",
        placeholder="e.g. Sucking your mom's nuts.",
        required=True,
        min_length=10,
        max_length=2000,
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        with open("cogs/jsonfiles/modmail.json", "r") as f:
            mod_mail = json.load(f)

        await interaction.response.send_message(
            f"{interaction.user.mention} Thank you for submitting your report, the moderation team will review it shortly.",
            ephemeral=True
        )

        mod_mail_channel = discord.utils.get(interaction.guild.channels, name=mod_mail[str(interaction.guild.id)])

        embed = discord.Embed(title=f"Mods, {interaction.user.name} Reported A User!",
                              color=discord.Color.yellow(),
                              timestamp=datetime.utcnow())
        embed.add_field(name="User Name:", value=self.user_name, inline=True)
        embed.add_field(name="User ID:", value=self.user_id, inline=True)
        embed.add_field(name="Report Reason:", value=self.description, inline=False)
        embed.set_thumbnail(url=interaction.user.avatar)

        await mod_mail_channel.send(embed=embed)

class Report(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()

    @app_commands.command(name="report", description="Report a user privately.")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ReportModal())

async def setup(client):
    await client.add_cog(Report(client))