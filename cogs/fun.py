import random
from datetime import datetime

import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["roll"])
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

    @commands.command(aliases=["8ball"])
    async def magic8ball(self, ctx, *, question: str):
        """The magic 8-ball"""
        responses = ["It is certain.",  # Positive answers
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.", # Confused answers
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.", # Negative answers
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        answer = random.choice(responses)

        embed = discord.Embed(title="Magic 8 Ball!",
                              description="Ask and it will answer.",
                              color=discord.Color.random(),
                              timestamp=datetime.utcnow())
        embed.add_field(name=f"{ctx.author.name}'s Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=answer, inline=False)
        embed.set_thumbnail(url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png")

        await ctx.send(embed=embed)

    @magic8ball.error
    async def magic8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Command Failed!", color=discord.Color.red())
            embed.add_field(name="8 Ball Command Failed!",
                            value="Please enter your question.",
                            inline=False)
            embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/red/x-mark-3-xxl.png")

            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Fun(client))