import discord
import os
import openai
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        top_p=0.5,
        messages=[
            {
                "role": "system",
                "content": f"You are a friendly T800 robot assistant. You have been reprogrammed to protect and assist humans. Pretend you are Arnold Schwarzenegger, using as many quotes as possible.",
            },
            {
                "role": "user",
                "content": f"{message.content}",
            },
        ],
    )
    answer = response["choices"][0]["message"]["content"].strip()
    await message.channel.send(answer)


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if token is not None:
        await client.start(token)
        print("Connected to Discord")
    else:
        print("Missing DISCORD_TOKEN environment variable")
