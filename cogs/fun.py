import random

import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll_dice(self, ctx, die_string: str):
        """Pray you won't get Nat 1."""
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 25:
            rolls = [random.randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        else:
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Dice Command Failed!",
                            value="Too many dice has been rolled. Please try a lower number.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

    @roll_dice.error
    async def roll_dice_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="Dice Command Failed!",
                            value="Please enter the dice amount. (eg. 1d6)",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Fun(client))