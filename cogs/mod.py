import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        if 0 < count <= 25:
            await ctx.message.delete()
            await ctx.channel.purge(limit=count)

            await ctx.send(f"Deleted {count} messages.")

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

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        user = discord.Object(userId)
        await ctx.guild.unban(user)

        embed = discord.Embed(title="Command Success!", color=discord.Color.green())
        embed.add_field(name="Member Unbanned!", value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}", inline=False)

        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Moderation(client))