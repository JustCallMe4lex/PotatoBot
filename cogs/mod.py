import json
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int = 1):
        if 0 < count <= 25:
            await ctx.message.delete()
            await ctx.channel.purge(limit=count)

            await ctx.send(f"Deleted {count} messages.")
        else:
            await ctx.message.delete()
            await ctx.send("Please enter the limit of messages in between 2 and 25.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        await ctx.guild.kick(member)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())

        fields = [("Member Kicked!", f"{member.mention} has been kicked from the server by {ctx.author.mention}.", "False"),
                  ("Reason:", reason, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Kick Member Failed!",
                            value="Please enter the member you wish to kick or enter a reason why.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        await ctx.guild.ban(member)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())

        fields = [
            ("Member Banned!", f"{member.mention} has been banned from the server by {ctx.author.mention}.", "False"),
            ("Reason:", reason, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Ban Member Failed!",
                            value="Please enter the member you wish to ban or enter a reason why.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(userId)
        await ctx.guild.unban(user)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Member Unbanned!",
                        value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}",
                        inline=False)

        await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Ban Member Failed!",
                            value="Please enter the ID of the member you want to unban.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        with open("cogs/json/mutes.json", "r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.add_roles(mute_role)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Member Muted!",
                        value=f"{member.mention} has been silenced from the server by {ctx.author.mention}",
                        inline=False)

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

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        with open("cogs/json/mutes.json", "r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        await member.remove_roles(mute_role)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Member Unmuted!",
                        value=f"{member.mention} has been unmuted from the server by {ctx.author.mention}",
                        inline=False)

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


async def setup(client):
    await client.add_cog(Moderation(client))