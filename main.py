from itertools import cycle
import os
import json
import asyncio

import discord
from discord.ext import commands, tasks

# File readers
with open("utils/token.0", "r", encoding="utf-8") as tf:
    TOKEN = tf.read()
with open("utils/owner_ids.0", "r", encoding="utf-8") as tf:
    OWNER_IDS = tf.read()

# Cycle Status
bot_status = cycle(["p!help for Commands", "Welcome to the server!"])


# Main Bot
client = commands.Bot(
    command_prefix="*",
    intents=discord.Intents.all(),
    owner_ids=OWNER_IDS
)

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    print("PotatoBot is connected and ready!")
    change_status.start()

@client.event
async def on_guild_join(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data[str(guild.id)] = {}
    data[str(guild.id)]['Channel'] = None
    data[str(guild.id)]['Message'] = None
    data[str(guild.id)]['AutoRole'] = None
    data[str(guild.id)]['ImageUrl'] = None

    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("cogs/json/welcome.json", "r") as f:
        data = json.load(f)

    data.pop(str(guild.id))

    with open("cogs/json/welcome.json", "w") as f:
        json.dump(data, f, indent=4)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} cog is now loaded and ready!")

async def main():
    async with client:
        print("Loading cogs...")
        await load()
        await client.start(TOKEN)

asyncio.run(main())