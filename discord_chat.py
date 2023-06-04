import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("I swear I will not kill anyone.")


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if token is not None:
        await client.start(token)
        print("Connected to Discord")
    else:
        print("Missing DISCORD_TOKEN environment variable")
