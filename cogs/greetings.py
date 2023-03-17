import json
import discord
from datetime import datetime
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        embed = discord.Embed(title=f"Welcome to the {member.guild.name} Server!",
                              description=f"You are the {member.guild.member_count} to hop in!",
                              color=discord.Colour.random())

        embed.add_field(name="A message from the admins: ", value=f"{data[str(member.guild.id)]['Message']}", inline=False)
        embed.set_image(url=data[str(member.guild.id)]["ImageUrl"])
        embed.set_footer(text=datetime.utcnow(), icon_url=member.avatar)

        # auto_role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]["AutoRole"])
        #
        # await member.add_roles(auto_role)

        if data[str(member.guild.id)]["Channel"] is None:
            await member.send(embed=embed)

        elif data[str(member.guild.id)]["Channel"] is not None:
            channel = discord.utils.get(member.guild.channels, name=data[str(member.guild.id)]["Channel"])
            await channel.send(embed=embed)

    @commands.group(name="greetings", invoke_without_command=True)
    async def greetings(self, ctx):
        embed = discord.Embed(title="Greeting System Setup",
                              description="Tweak and adjust the welcome system here!",
                              color=discord.Colour.random())

        fields = [("Auto Role", "Set an automatic role so when a user joins, they will receive it automatically.", False),
                  ("Message", "Set a message to be included in the welcome card.", False),
                  ("Channel", "Set a channel for the welcome card to be sent in.", False),
                  ("Image URL", "Set an image or gif url to be sent with the welcome card.", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @greetings.command()
    async def autorole(self, ctx, role: discord.Role):
        if role == None:
            await ctx.send("Please input the ID of the role.")

        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["AutoRole"] = str(role.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Auto Role has been changed to || {role.name} ||.")

    @greetings.command()
    async def message(self, ctx, *, message):
        if message == None:
            await ctx.send("Please input the message for the welcome card.")

        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Message"] = str(message)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send("Greeting message has been changed.")

    @greetings.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if channel == None:
            await ctx.send("Please input the ID of the channel.")

        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Channel has been changed to || {channel.name} ||.")

    @greetings.command()
    async def imageurl(self, ctx, *, url):
        if url == None:
            await ctx.send("Please input the URL of the image for the welcome card.")

        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["ImageUrl"] = str(url)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send("Card Image has been changed.")


async def setup(client):
    await client.add_cog(Greetings(client))