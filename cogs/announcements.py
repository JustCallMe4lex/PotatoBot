import json
from datetime import datetime

import discord
from discord.ext import commands

class Announcements(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, announcement):
        with open("cogs/jsonfiles/announcements.json", "r") as f:
            ann_data = json.load(f)

        announce_channel = discord.utils.get(ctx.guild.channels, name=ann_data[str(ctx.guild.id)])

        embed = discord.Embed(title="Listen Up!",
                              description="They aboutta say something.",
                              color=discord.Color.blue(),
                              timestamp=datetime.utcnow())
        embed.add_field(name="Announcement:", value=f"@everyone, {announcement}", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar)

        await announce_channel.send(embed=embed)

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Announce Command Failed!",
                            value="Please enter your message.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Announce Command Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)



async def setup(client):
    await client.add_cog(Announcements(client))