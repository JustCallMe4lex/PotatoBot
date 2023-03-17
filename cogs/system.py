import json

import discord
from discord.ext import commands

class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def greet_settings(self, ctx):
        embed = discord.Embed(title="Greeting System Setup",
                              description="Tweak and adjust the welcome system here!",
                              color=discord.Colour.random())

        fields = [
            ("Auto Role", "Set an automatic role so when a user joins, they will receive it automatically.", False),
            ("Message", "Set a message to be included in the welcome card.", False),
            ("Channel", "Set a channel for the welcome card to be sent in.", False),
            ("Image URL", "Set an image or gif url to be sent with the welcome card.", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @greet_settings.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["AutoRole"] = str(role.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Auto Role Set!",
                        value=f"Mute role has been changed to `{role.mention}`.",
                        inline=False)

        await ctx.send(embed=embed)

    @autorole.error
    async def autorole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Auto Role Set Failed!",
                            value="Please enter the ID of the role.",
                            inline=False)

            await ctx.send(embed=embed)


    @greet_settings.command()
    @commands.has_permissions(administrator=True)
    async def message(self, ctx, *, message):
        if 10 < len(message) <= 200:
            with open("cogs/json/welcome.json", "r") as f:
                data = json.load(f)

            data[str(ctx.guild.id)]["Message"] = str(message)

            with open("cogs/json/welcome.json", "w") as f:
                json.dump(data, f, indent=4)

            embed = discord.Embed(title="Command Success!", color=discord.Color.green())
            embed.add_field(name="Welcome Message Set!",
                            value=f"Message has been changed to `{message}`.",
                            inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Welcome Message Set Failed!",
                            value="Enter your message between 10 to 200 characters.",
                            inline=False)

            await ctx.send(embed=embed)

    @message.error
    async def message_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Welcome Message Set Failed!",
                            value="Please enter your desired welcome message.",
                            inline=False)

            await ctx.send(embed=embed)

    @greet_settings.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Welcome Channel Set!",
                        value=f"Channel has been changed to `{channel.name}`.",
                        inline=False)

        await ctx.send(embed=embed)

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Channel Set Failed!",
                            value="Please enter a channel.",
                            inline=False)

            await ctx.send(embed=embed)

    @greet_settings.command()
    @commands.has_permissions(administrator=True)
    async def imageurl(self, ctx, *, url):
        with open("cogs/json/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["ImageUrl"] = str(url)

        with open("cogs/json/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Welcome Image Set!",
                        value=f"Image has been changed to `{url}`.",
                        inline=False)

        await ctx.send(embed=embed)

    @imageurl.error
    async def imageurl_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Image Set Failed!",
                            value="Please enter a URL.",
                            inline=False)

            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.client.latency * 1000)

        await ctx.send(f"Pong! {bot_latency}ms")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, *, newprefix: str):
        if 0 < len(newprefix) <= 5:
            with open("cogs/json/prefix.json.", "r") as f:
                prefix = json.load(f)

            prefix[str(ctx.guild.id)] = newprefix

            with open("cogs/json/prefix.json", "w") as f:
                json.dump(prefix, f, indent=4)

            embed = discord.Embed(title="Command Success!", color=discord.Color.green())
            embed.add_field(name="Change Prefix Set!",
                            value=f"Prefix has been changed to `{newprefix}`.",
                            inline=False)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Change Prefix Failed!",
                            value="Please enter characters between 1 and 5.",
                            inline=False)

            await ctx.send(embed=embed)

    @change_prefix.error
    async def change_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Change Prefix Failed!",
                            value="Please enter a character/s.",
                            inline=False)

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmuterole(self, ctx, role: discord.Role):
        with open("cogs/json/mutes.json", "r") as f:
            mutes = json.load(f)

        mutes[str(ctx.guild.id)] = role.name

        with open("cogs/json/mutes.json", "w") as f:
            json.dump(mutes, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Mute Role Set!",
                        value=f"Mute role has been changed to `{role.mention}`. All members who are muted will have this role.",
                        inline=False)

        await ctx.send(embed=embed)

    @setmuterole.error
    async def setmuterole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Role Set Failed!",
                            value="Please enter the ID of the role.",
                            inline=False)

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(System(client))