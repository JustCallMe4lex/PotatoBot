import json
import discord
from datetime import datetime
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("cogs/jsonfiles/welcome.json", "r") as f:
            data = json.load(f)

        embed = discord.Embed(title=f"Welcome to the {member.guild.name} Server!",
                              description=f"You are member #{member.guild.member_count}!",
                              color=discord.Colour.random())

        embed.add_field(name="A message from the admins: ", value=f"{data[str(member.guild.id)]['Message']}", inline=False)
        embed.set_image(url=data[str(member.guild.id)]["ImageUrl"])
        embed.set_footer(text=datetime.utcnow(), icon_url=member.avatar)

        if data[str(member.guild.id)]["Channel"] is None:
            await member.send(embed=embed)

        elif data[str(member.guild.id)]["Channel"] is not None:
            channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])
            await channel.send(embed=embed)

        auto_role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]["AutoRole"])

        await member.add_roles(auto_role)


async def setup(client):
    await client.add_cog(Greetings(client))