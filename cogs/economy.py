import json
import random

import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        with open("cogs/json/economy.json", "r") as f:
            user_eco = json.load(f)

        with open("cogs/json/prefix.json", "r") as f:
            prefix = json.load(f)

        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        if str(member.id) not in user_eco:
            user_eco[str(member.id)] = {}
            user_eco[str(member.id)]["Balance"] = 0
            user_eco[str(member.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        embed = discord.Embed(title=f"{member.name}'s Current Balance",
                              description=f"The amount of coins on {member.name}.",
                              color=discord.Color.random())
        embed.add_field(name="Coins:", value=f"{user_eco[str(member.id)]['Balance']}", inline=False)
        embed.set_footer(text=f"Want to add more coins to your pocket? Use economy commands like {prefix[str(ctx.guild.id)]}daily or {prefix[str(ctx.guild.id)]}work.")
        embed.set_thumbnail(url=member.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        with open("cogs/json/economy.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 0
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        amount = random.randint(50, 100)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("cogs/json/economy.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        embed = discord.Embed(title="Work Is Done!",
                              description="After a tiring shift, here's what you have garnered!",
                              color=discord.Color.random())
        embed.add_field(name="Earnings:", value=f"{amount} coins", inline=False)
        embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']} coins", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Work Command Failed!",
                            value=f"You have already used this command. Please come back after an hour.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        with open("cogs/json/economy.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 0
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        amount = random.randint(100, 300)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("cogs/json/economy.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        embed = discord.Embed(title="Daily Coins!",
                              description="Here's your daily bonus!",
                              color=discord.Color.random())
        embed.add_field(name="Earnings:", value=f"{amount} coins", inline=False)
        embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']} coins", inline=False)
        embed.set_thumbnail(url=ctx.author.avatar)

        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Daily Command Failed!",
                            value="You have claimed your daily bonus. Please come back tomorrow.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    # @commands.command()
    # async def slots(self, ctx, coins):
    #     with open("cogs/json/economy.json", "r") as f:
    #         user_eco = json.load(f)
    #
    #     if str(ctx.author.id) not in user_eco:
    #         user_eco[str(ctx.author.id)] = {}
    #         user_eco[str(ctx.author.id)]["Balance"] = 100
    #         user_eco[str(ctx.author.id)]["Bank"] = 0
    #
    #         with open("cogs/json/economy.json", "w") as f:
    #             json.dump(user_eco, f, indent=4)
    #
    #     choices = [":heart:", ":blue_heart:", ":orange_heart:"]
    #
    #     slot1 = random.choice(choices)
    #     slot2 = random.choice(choices)
    #     slot3 = random.choice(choices)
    #
    #     fields = [("Slot 1", f"{slot1}", True),
    #               ("Slot 2", f"{slot2}", True),
    #               ("Slot 3", f"{slot3}", True)]
    #
    #     if slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
    #
    #         embed = discord.Embed(title="Slot Machine!",
    #                               description="Gamble your coins to double it, triple it or lose it!",
    #                               color=discord.Color.random())
    #
    #         embed.add_field(name="Win!", value=f"You won {coins * 2} coins!", inline=False)
    #
    #         for name, value, inline in fields:
    #             embed.add_field(name=name, value=value, inline=inline)
    #
    #         embed.add_field(name="Earnings:", value=f"{coins * 2} coins", inline=False)
    #         embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance'] * 2} coins", inline=False)
    #         embed.set_thumbnail(url=ctx.author.avatar)
    #
    #         await ctx.send(embed=embed)
    #     elif slot1 == slot2 == slot3:
    #         amount = coins * 3
    #
    #         embed = discord.Embed(title="Slot Machine!",
    #                               description="Gamble your coins to double it, triple it or lose it!",
    #                               color=discord.Color.random())
    #
    #         embed.add_field(name="Big Win!", value=f"You won {amount} coins!", inline=False)
    #
    #         for name, value, inline in fields:
    #             embed.add_field(name=name, value=value, inline=inline)
    #
    #         embed.add_field(name="Earnings:", value=f"{amount} coins", inline=False)
    #         embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']} coins", inline=False)
    #         embed.set_thumbnail(url=ctx.author.avatar)
    #
    #         await ctx.send(embed=embed)
    #     else:
    #         embed = discord.Embed(title="Slot Machine!",
    #                               description="Gamble your coins to double it, triple it or lose it!",
    #                               color=discord.Color.random())
    #
    #         embed.add_field(name="Lose!", value=f"You lost {coins} coins!", inline=False)
    #
    #         for name, value, inline in fields:
    #             embed.add_field(name=name, value=value, inline=inline)
    #
    #         embed.add_field(name="Lost Coins:", value=f"{coins} coins", inline=False)
    #         embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']} coins", inline=False)
    #         embed.set_thumbnail(url=ctx.author.avatar)
    #
    #         await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Economy(client))