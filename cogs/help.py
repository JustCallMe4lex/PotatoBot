from datetime import datetime

import discord
from discord.ext import commands

class PotatoHelpCommand(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    def get_command_signature(self, command):
        return '{0.context.prefix}{1.qualified_name} {1.signature}'.format(self, command)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Potato Help Menu",
                              description="Here are the available commands down below!",
                              colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)

            if filtered:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(c.name for c in filtered), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name,
                              colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            embed.description = "\n".join(c.name for c in filtered)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name,
                              colour=discord.Colour.random(),
                              timestamp=datetime.utcnow())

        filtered = await self.filter_commands(group.commands, sort=True)
        if filtered:
            embed.description = "\n".join(c.name for c in filtered)
            embed.add_field(name="Usage:", value=self.get_command_signature(group))

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Command: {command.qualified_name}",
                              description=f"Here's what the **{command.qualified_name}** command do!",
                              colour=discord.Colour.blurple(),
                              timestamp=datetime.utcnow())

        embed.add_field(name="Usage:", value=self.get_command_signature(command))

        if command.help:
            embed.add_field(name="Description:", value=command.help)

        if command.aliases:
            embed.add_field(name="Aliases:", value=", ".join(command.aliases))

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        channel = self.get_destination()
        await channel.send(error)

async def setup(client):
    client.help_command = PotatoHelpCommand()