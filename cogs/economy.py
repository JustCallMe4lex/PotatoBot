import json
import random

import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your coin balance"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        with open("cogs/jsonfiles/prefix.json", "r") as f:
            prefix = json.load(f)

        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        if str(member.id) not in user_eco:
            user_eco[str(member.id)] = {}
            user_eco[str(member.id)]["Balance"] = 100
            user_eco[str(member.id)]["Bank"] = 0

            with open("cogs/jsonfiles/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        embed = discord.Embed(title=f"{member.name}'s Current Balance",
                              description=f"The amount of coins on {member.name}.",
                              color=discord.Color.random())
        embed.add_field(name="Coins:", value=f"{user_eco[str(member.id)]['Balance']}", inline=True)
        embed.add_field(name="Bank:", value=f"{user_eco[str(member.id)]['Bank']}", inline=True)
        embed.set_footer(text=f"Want to add more coins to your pocket? Use economy commands like {prefix[str(ctx.guild.id)]}daily or {prefix[str(ctx.guild.id)]}work.")
        embed.set_thumbnail(url=member.avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        """Work for coins"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/jsonfiles/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        amount = random.randint(50, 100)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("cogs/jsonfiles/economy.json", "w") as f:
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
        """Daily bonus coins"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        with open("cogs/jsonfiles/prefix.json", "r") as f:
            prefix = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        amount = random.randint(100, 300)

        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("cogs/jsonfiles/economy.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        embed = discord.Embed(title="Daily Coins!",
                              description="Here's your daily bonus!",
                              color=discord.Color.random())
        embed.add_field(name="Earnings:", value=f"{amount} coins", inline=False)
        embed.add_field(name="New Balance:", value=f"{user_eco[str(ctx.author.id)]['Balance']} coins", inline=False)
        embed.set_footer(text=f"Want to keep your moolah safe? Use {prefix[str(ctx.guild.id)]}deposit to hide your coins in the bank.")
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

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        """Steal another user's coins"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        steal_prob = random.randint(0, 1)

        if steal_prob == 1: # Steal!!
            amount = random.randint(1, 25)

            if str(ctx.author.id) not in user_eco:
                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Bank"] = 0

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            elif str(member.id) not in user_eco:
                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]["Balance"] = 100
                user_eco[str(member.id)]["Bank"] = 0

                with open("cogs/jsonfiles/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            if amount > user_eco[str(member.id)]["Balance"]:
                await ctx.send("So... You're stealing from a poor person? Shameful.")
            else:
                user_eco[str(ctx.author.id)]["Balance"] += amount
                user_eco[str(member.id)]["Balance"] -= amount
                with open("cogs/jsonfiles/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

                await ctx.send(f"Looks you get away with {amount} coins from {member.mention} this time.")

        else:
            await ctx.send("Looks like you were caught. Better luck next time.")

    @steal.error
    async def steal_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Steal Command Failed!",
                            value="Please enter the member you wish to kick or enter a reason why.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Steal Command Failed!",
                            value="Take a break. You can steal after a minute again.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command(aliases=["dp"])
    async def deposit(self, ctx, amount: int):
        """Deposit coins into the bank"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        if amount > user_eco[str(ctx.author.id)]["Balance"]:
            await ctx.send("Insufficient balance.")
        else:
            user_eco[str(ctx.author.id)]["Bank"] += amount
            user_eco[str(ctx.author.id)]["Balance"] -= amount
            with open("cogs/jsonfiles/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

            await ctx.send(f"Successfully deposited {amount} coins into the bank.")

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Deposit Command Failed!",
                            value="Enter amount of coins to be deposited.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command(aliases=["wd"])
    async def withdraw(self, ctx, amount: int):
        """Withdraw your coins from the bank"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Bank"] = 0

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        if amount > user_eco[str(ctx.author.id)]["Bank"]:
            await ctx.send("Insufficient balance.")
        else:
            user_eco[str(ctx.author.id)]["Bank"] -= amount
            user_eco[str(ctx.author.id)]["Balance"] += amount
            with open("cogs/jsonfiles/economy.json", "w") as f:
                json.dump(user_eco, f, indent=4)

            await ctx.send(f"Successfully withdrawn {amount} coins from the bank.")

    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Withdraw Command Failed!",
                            value="Enter amount of coins to be withdrawn.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

    @commands.command()
    async def slots(self, ctx, amount: int):
        """Gamble your coins"""
        with open("cogs/jsonfiles/economy.json", "r") as f:
            user_eco = json.load(f)

        final = []
        for i in range(3):
            a = random.choice([":heart:", ":blue_heart:", ":yellow_heart:", ":green_heart:", ":orange_heart:"])
            final.append(a)

        if final[0] == final[1] == final[2]: # All 3 slots match
            winnings = amount * 3

            if str(ctx.author.id) not in user_eco:
                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Bank"] = 0

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            if amount > user_eco[str(ctx.author.id)]["Balance"]:
                await ctx.send("Insufficient balance.")
            else:
                user_eco[str(ctx.author.id)]["Balance"] += winnings
                with open("cogs/jsonfiles/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

                embed = discord.Embed(title="Slot Machine!",
                                      description="Win tripe, double or lose it all.",
                                      color=discord.Color.random())
                embed.add_field(name="Slot 1", value=final[0], inline=True)
                embed.add_field(name="Slot 2", value=final[1], inline=True)
                embed.add_field(name="Slot 3", value=final[2], inline=True)
                embed.add_field(name="Jackpot!", value=f"You won {winnings} coins!", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar)

                await ctx.send(embed=embed)

        elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]: # 2 slots match
            winnings = amount * 2

            if str(ctx.author.id) not in user_eco:
                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Bank"] = 0

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            if amount > user_eco[str(ctx.author.id)]["Balance"]:
                await ctx.send("Insufficient balance.")
            else:
                user_eco[str(ctx.author.id)]["Balance"] += winnings
                with open("cogs/jsonfiles/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

                embed = discord.Embed(title="Slot Machine!",
                                      description="Win tripe, double or lose it all.",
                                      color=discord.Color.random())
                embed.add_field(name="Slot 1", value=final[0], inline=True)
                embed.add_field(name="Slot 2", value=final[1], inline=True)
                embed.add_field(name="Slot 3", value=final[2], inline=True)
                embed.add_field(name="Winner!", value=f"You won {winnings} coins!", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar)

                await ctx.send(embed=embed)

        else: # None match
            if str(ctx.author.id) not in user_eco:
                user_eco[str(ctx.author.id)] = {}
                user_eco[str(ctx.author.id)]["Balance"] = 100
                user_eco[str(ctx.author.id)]["Bank"] = 0

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

            if amount > user_eco[str(ctx.author.id)]["Balance"]:
                await ctx.send("Insufficient balance.")
            else:
                user_eco[str(ctx.author.id)]["Balance"] -= amount
                with open("cogs/jsonfiles/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

                embed = discord.Embed(title="Slot Machine!",
                                      description="Win tripe, double or lose it all.",
                                      color=discord.Color.random())
                embed.add_field(name="Slot 1", value=final[0], inline=True)
                embed.add_field(name="Slot 2", value=final[1], inline=True)
                embed.add_field(name="Slot 3", value=final[2], inline=True)
                embed.add_field(name="Loser!", value=f"You lost {amount} coins!", inline=False)
                embed.set_thumbnail(url=ctx.author.avatar)

                await ctx.send(embed=embed)

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Slots Command Failed!",
                            value="Enter amount of coins to gamble.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Economy(client))