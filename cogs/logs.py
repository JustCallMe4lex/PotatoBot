from datetime import datetime
import json

import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, before, after): # User changes name, disc or avatar
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(after.guild.channels, name=logs[str(after.guild.id)])

        if before.name != after.name:
            embed = discord.Embed(title="Username Changed!",
                                  description=f"{after.name} has changed their name!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.add_field(name="Before:", value=before.name, inline=False)
            embed.add_field(name="After:", value=after.name, inline=False)
            embed.set_thumbnail(url=after.avatar)

            await log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = discord.Embed(title="Discriminator Changed!",
                                  description=f"{after.name} has changed their discriminator!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.add_field(name="Before:", value=before.discriminator, inline=False)
            embed.add_field(name="After:", value=after.discriminator, inline=False)
            embed.set_thumbnail(url=after.avatar)

            await log_channel.send(embed=embed)

        if before.avatar != after.avatar:
            embed = discord.Embed(title="Avatar Changed!",
                                  description=f"{after.name} has changed their avatar!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.set_thumbnail(url=before.avatar)
            embed.set_image(url=after.avatar)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(after.guild.channels, name=logs[str(after.guild.id)])

        if before.display_name != after.display_name:
            embed = discord.Embed(title="Nickname Changed!",
                                  description=f"{after.name} has changed their nickname!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.add_field(name="Before:", value=before.display_name, inline=False)
            embed.add_field(name="After:", value=after.display_name, inline=False)
            embed.set_thumbnail(url=after.avatar)

            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = discord.Embed(title="Roles Updated!",
                                  description=f"{after.name} has updated their roles!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.add_field(name="Before:", value=", ".join([r.mention for r in before.roles]), inline=False)
            embed.add_field(name="After:", value=", ".join([r.mention for r in after.roles]), inline=False)
            embed.set_thumbnail(url=after.avatar)

            await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member): # Member leaves the server
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Joined!",
                              description="A new challenger approaches!",
                              color=discord.Color.blue(),
                              timestamp=datetime.utcnow())
        embed.add_field(name="User:", value=member.mention, inline=False)
        embed.set_thumbnail(url=member.avatar)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member): # Member leaves the server
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(member.guild.channels, name=logs[str(member.guild.id)])

        embed = discord.Embed(title="Member Left!",
                              description="A user has passed along to a better one!",
                              color=discord.Color.blue(),
                              timestamp=datetime.utcnow())
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
                                      color=discord.Color.blue(),
                                      timestamp=datetime.utcnow())
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
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())
            embed.add_field(name="Message Deleted:", value=message.content, inline=False)
            embed.set_thumbnail(url=message.author.avatar)

            await log_channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Logs(client))
