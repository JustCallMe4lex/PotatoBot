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

# Grabbing the Server Prefix
def get_server_prefix(client, message):
    with open("cogs/jsonfiles/prefix.json", "r") as f:
        prefix = json.load(f)

    return prefix[str(message.guild.id)]

# Main Bot
client = commands.Bot(
    command_prefix=get_server_prefix,
    intents=discord.Intents.all(),
    owner_ids=OWNER_IDS
)

# Looping the Activity
@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    print("PotatoBot is connected and ready!")
    change_status.start()

@client.event
async def on_guild_join(guild):
    # Adding Guild to Welcome Data
    with open("cogs/jsonfiles/welcome.json", "r") as f:
        data = json.load(f)

    data[str(guild.id)] = {}
    data[str(guild.id)]['Channel'] = None
    data[str(guild.id)]['Message'] = None
    data[str(guild.id)]['AutoRole'] = None
    data[str(guild.id)]['ImageUrl'] = None

    with open("cogs/jsonfiles/welcome.json", "w") as f:
        json.dump(data, f, indent=4)

    # Adding Guild to Prefix Data
    with open("cogs/jsonfiles/prefix.json.", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "p!"

    with open("cogs/jsonfiles/prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)

    # Adding Guild to Mutes Data
    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mutes = json.load(f)

    mutes[str(guild.id)] = None

    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mutes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    # Removing Welcome Data
    with open("cogs/jsonfiles/welcome.json", "r") as f:
        data = json.load(f)

    data.pop(str(guild.id))

    with open("cogs/jsonfiles/welcome.json", "w") as f:
        json.dump(data, f, indent=4)

    # Removing Prefix Data
    with open("cogs/jsonfiles/prefix.json.", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("cogs/jsonfiles/prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)

    # Removing Mutes Data
    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mutes = json.load(f)

    mutes.pop(str(guild.id))

    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mutes, f, indent=4)

# Loading Cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} cog is now loaded and ready!")

# Main Async Function
async def main():
    async with client:
        print("Loading cogs...")
        await load()
        await client.start(TOKEN)

asyncio.run(main())