import json
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, members: commands.Greedy[discord.Member],  count: Optional[int] = 1, reason: Optional[int] = None):
        """Clear some messages"""
        def _check(message):
            return not len(members) or message.author in members

        if 0 < count <= 25:
            async with ctx.channel.typing():
                await ctx.message.delete()
                await ctx.channel.purge(limit=count, check=_check, reason=reason)

                await ctx.send(f"Deleted {count} messages.")
        else:
            await ctx.message.delete()
            await ctx.send("Please enter the limit of messages in between 2 and 25.")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Clear Command Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        """Kick a member"""
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(ctx.guild.channels, name=logs[str(ctx.guild.id)])

        await ctx.guild.kick(member)

        kick_embed = discord.Embed(title="Command Success!", color=discord.Color.green())

        fields = [("Member Kicked!", f"{member.mention} has been kicked from the server by {ctx.author.mention}.", False),
                  ("Reason:", reason, False)]

        for name, value, inline in fields:
            kick_embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=kick_embed)

        log_embed = discord.Embed(title="A member has been booted off the server!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())

        log_embed.add_field(name="Kicked Member:", value=f"{member.mention}", inline=False)
        log_embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        log_embed.set_thumbnail(url=member.avatar)

        await log_channel.send(embed=log_embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Kick Member Failed!",
                            value="Please enter the member you wish to kick or enter a reason why.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Kick Member Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        """Ban a member"""
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(ctx.guild.channels, name=logs[str(ctx.guild.id)])

        await ctx.guild.ban(member)

        ban_embed = discord.Embed(title="Command Success!", color=discord.Color.green())

        fields = [
            ("Member Banned!", f"{member.mention} has been banned from the server by {ctx.author.mention}.", False),
            ("Reason:", reason, False)]

        for name, value, inline in fields:
            ban_embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=ban_embed)

        log_embed = discord.Embed(title="The ban hammer has been brought down to a member!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())

        log_embed.add_field(name="Ban Member:", value=f"{member.mention}", inline=False)
        log_embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        log_embed.set_thumbnail(url=member.avatar)

        await log_channel.send(embed=log_embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Ban Member Failed!",
                            value="Please enter the member you wish to ban or enter a reason why.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Ban Member Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        """Unban a member"""
        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(ctx.guild.channels, name=logs[str(ctx.guild.id)])

        user = discord.Object(userId)
        await ctx.guild.unban(user)

        unban_embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        unban_embed.add_field(name="Member Unbanned!",
                        value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}.",
                        inline=False)

        await ctx.send(embed=unban_embed)

        log_embed = discord.Embed(title="A member has been unbanned in the server!",
                                  color=discord.Color.blue(),
                                  timestamp=datetime.utcnow())

        log_embed.add_field(name="User ID:", value=f"{userId}", inline=False)

        await log_channel.send(embed=log_embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Unban Member Failed!",
                            value="Please enter the ID of the member you want to unban.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Unban Member Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        """Mute a member"""
        with open("cogs/jsonfiles/mutes.json", "r") as f:
            role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(ctx.guild.channels, name=logs[str(ctx.guild.id)])

        if mute_role is not None:
            await member.add_roles(mute_role)

            embed = discord.Embed(title="Command Success!", color=discord.Color.green())
            embed.add_field(name="Member Muted!",
                            value=f"{member.mention} has been silenced from the server by {ctx.author.mention}.",
                            inline=False)

            await ctx.send(embed=embed)

            log_embed = discord.Embed(title="A member has been silenced the server!",
                                      color=discord.Color.blue(),
                                      timestamp=datetime.utcnow())

            log_embed.add_field(name="Muted Member:", value=f"{member.mention}", inline=False)
            log_embed.set_thumbnail(url=member.avatar)

            await log_channel.send(embed=log_embed)
        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Member Failed!",
                            value="No mute role detected. Please enter a role.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Member Failed!",
                            value="Please enter the member you wish to silence.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Member Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        with open("cogs/jsonfiles/mutes.json", "r") as f:
            role = json.load(f)

        mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        with open("cogs/jsonfiles/logs.json", "r") as f:
            logs = json.load(f)

        log_channel = discord.utils.get(ctx.guild.channels, name=logs[str(ctx.guild.id)])

        if mute_role is not None:
            await member.remove_roles(mute_role)

            embed = discord.Embed(title="Command Success!", color=discord.Color.green())
            embed.add_field(name="Member Unmuted!",
                            value=f"{member.mention} has been unmuted from the server by {ctx.author.mention}.",
                            inline=False)

            await ctx.send(embed=embed)

            log_embed = discord.Embed(title="A member has been unmuted in the server!",
                                      color=discord.Color.blue(),
                                      timestamp=datetime.utcnow())

            log_embed.add_field(name="Unmuted Member:", value=f"{member.mention}", inline=False)
            log_embed.set_thumbnail(url=member.avatar)

            await log_channel.send(embed=log_embed)
        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Mute Member Failed!",
                            value="No mute role detected. Please enter a mute role.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Unmute Member Failed!",
                            value="Please enter the member you wish to unmute.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Unmute Member Failed!",
                            value="You don't have the required permissions to use this command.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Moderation(client))