import json

import discord
from discord.ext import commands

class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """Adjust the settings of the server"""
        with open("cogs/jsonfiles/prefix.json", "r") as f:
            prefix = json.load(f)

        embed = discord.Embed(title="System Setup",
                              description="Tweak and adjust the server settings here!",
                              color=discord.Colour.random())

        fields = [
            ("Auto Role", "Set an automatic role so when a user joins, they will receive it automatically.", False),
            ("Welcome Message", "Set a message to be included in the welcome card.", False),
            ("Welcome Channel", "Set a channel for the welcome card to be sent in.", False),
            ("Image URL", "Set an image or gif url to be sent with the welcome card.", False),
            ("Server Prefix", f"The current prefix is `{prefix[str(ctx.guild.id)]}`. You can change it if you wish", False),
            ("Mute Role", "Set a mute role to mute members.", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def setautorole(self, ctx, role: discord.Role):
        """Set the welcome role"""
        with open("cogs/jsonfiles/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["AutoRole"] = str(role.name)

        with open("cogs/jsonfiles/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Auto Role Set!",
                        value=f"Auto role has been changed to {role.mention}.",
                        inline=False)

        await ctx.send(embed=embed)

    @setautorole.error
    async def autorole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Auto Role Set Failed!",
                            value="Please enter the ID of the role.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Auto Role Set Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


    @settings.command()
    @commands.has_permissions(administrator=True)
    async def setwelcomemessage(self, ctx, *, message):
        """Set the welcome message"""
        if 10 < len(message) <= 200:
            with open("cogs/jsonfiles/welcome.json", "r") as f:
                data = json.load(f)

            data[str(ctx.guild.id)]["Message"] = str(message)

            with open("cogs/jsonfiles/welcome.json", "w") as f:
                json.dump(data, f, indent=4)

            embed = discord.Embed(title="Command Success!", color=discord.Color.green())
            embed.add_field(name="Welcome Message Set!",
                            value=f"Message has been changed to {message}.",
                            inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Welcome Message Set Failed!",
                            value="Enter your message between 10 to 200 characters.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @setwelcomemessage.error
    async def setwelcomemessage_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Welcome Message Set Failed!",
                            value="Please enter your desired welcome message.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Welcome Message Set Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        """Set the welcome channel"""
        with open("cogs/jsonfiles/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["Channel"] = str(channel.name)

        with open("cogs/jsonfiles/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Welcome Channel Set!",
                        value=f"Channel has been changed to {channel.name}.",
                        inline=False)

        await ctx.send(embed=embed)

    @setwelcomechannel.error
    async def setwelcomechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Channel Set Failed!",
                            value="Please enter a channel.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Channel Set Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def setimageurl(self, ctx, *, url):
        """Set the welcome image"""
        with open("cogs/jsonfiles/welcome.json", "r") as f:
            data = json.load(f)

        data[str(ctx.guild.id)]["ImageUrl"] = str(url)

        with open("cogs/jsonfiles/welcome.json", "w") as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Welcome Image Set!",
                        value=f"Image has been changed to `{url}`.",
                        inline=False)

        await ctx.send(embed=embed)

    @setimageurl.error
    async def setimageurl_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Image Set Failed!",
                            value="Please enter a URL.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Image Set Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Check ping"""
        bot_latency = round(self.client.latency * 1000)

        await ctx.send(f"Pong! {bot_latency}ms")

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, *, newprefix: str):
        """Change the prefix of the server"""
        if 0 < len(newprefix) <= 5:
            with open("cogs/jsonfiles/prefix.json.", "r") as f:
                prefix = json.load(f)

            prefix[str(ctx.guild.id)] = newprefix

            with open("cogs/jsonfiles/prefix.json", "w") as f:
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

    @changeprefix.error
    async def changeprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Change Prefix Failed!",
                            value="Please enter a character/s.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Change Prefix Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @settings.command()
    @commands.has_permissions(administrator=True)
    async def setmuterole(self, ctx, role: discord.Role):
        """Set the mute role for the mute command"""
        with open("cogs/jsonfiles/mutes.json", "r") as f:
            mutes = json.load(f)

        mutes[str(ctx.guild.id)] = role.name

        with open("cogs/jsonfiles/mutes.json", "w") as f:
            json.dump(mutes, f, indent=4)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Mute Role Set!",
                        value=f"Mute role has been changed to {role.mention}. All members who are muted will have this role.",
                        inline=False)

        await ctx.send(embed=embed)

    @setmuterole.error
    async def setmuterole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Role Set Failed!",
                            value="Please enter the ID of the role.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Role Set Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(System(client))