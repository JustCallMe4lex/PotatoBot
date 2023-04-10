import json

import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member): # Member leaves the server
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Joined!",
                              description="A new challenger approaches!",
                              color=discord.Color.blue())
        embed.add_field(name="User:", value=member.mention, inline=False)
        embed.set_thumbnail(url=member.avatar)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member): # Member leaves the server
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Left!",
                              description="A user left da hood!",
                              color=discord.Color.blue())
        embed.add_field(name="User:", value=member.mention, inline=False)
        embed.add_field(url=member.avatar)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after): # Member edits message
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(after.author.guild.channels, name=logs[str(after.author.guild.id)])

        if not after.author.bot:
            if before.content != after.content:
                embed = discord.Embed(title="Message Edited!",
                                      description=f"{after.author.display_name} has been editing messages.",
                                      color=discord.Color.blue())
                embed.add_field(name="Message Before:", value=before.content, inline=False)
                embed.add_field(name="Message After:", value=after.content, inline=False)
                embed.set_thumbnail(url=after.author.avatar)

                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):  # Member deletes message
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(message.author.guild.channels, name=logs[str(message.author.guild.id)])

        if not message.author.bot:
            embed = discord.Embed(title="Message Deleted!",
                                  description=f"{message.author.display_name} has been deleting messages.",
                                  color=discord.Color.blue())
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.set_thumbnail(url=message.author.avatar)

            await log_channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Logs(client))
