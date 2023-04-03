import json

import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Joined!",
                              description="A new challenger approaches!",
                              color=discord.Color.blue())
        embed.add_field(name="User:", value=member.mention, inline=False)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Left!",
                              description="A user left da hood!",
                              color=discord.Color.blue())
        embed.add_field(name="User:", value=member.mention, inline=False)

        await log_channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Logs(client))
