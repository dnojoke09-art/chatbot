import os
import discord
import requests
import json

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # <- use env variable
GROQ_KEY = os.getenv("GROQ_API_KEY")    # <- use env variable
MODEL = "llama3"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def groq_chat(prompt):
    url = f"https://api.groq.com/v1/models/{MODEL}/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Sorry, I couldn't generate a response."

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prompt = message.content
    reply = groq_chat(prompt)
    await message.channel.send(reply)

client.run(TOKEN)