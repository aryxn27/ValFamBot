import os
from http.client import responses
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio


#loading environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('VAL_FAM_ID'))
GEMINI_KEY = os.getenv('GEMINI_KEY')

intents = discord.Intents.default()
intents.message_content = True

#AI setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

async def call_gemini(prompt: str) -> str:
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"



#response dictionary
RESPONSES = {
    "jared": "Greatest Scottish man of all time",
    "niamh": "Greatest Scottish woman of all time",
    "valorant": "Why don't we play rivals instead?",
    "rivals": "Best game ever btw",
    "emily": "Bug lady 🐞",
    "tash": "Group mum",
    "bekim": "Nazi",
    "aryan": "greatest human being alive",
    "phantom": "greatest human being alive",
    "anyone on": "in other words 'someone play with me im lonely'",
    "fuck": "do you think swearing makes you cool?",
    "fucks": "do you think swearing makes you cool?",
    "shit": "do you think swearing makes you cool?",
    "piss": "do you think swearing makes you cool?",
    "cunt": "do you think swearing makes you cool?",
    "hi bot": "fuck off (sorry aryan makes me say that I actually love you guys :(",
    "sean": "the unc",
    "ava": "aryan (my master) does not know you well enough to feel comfortable insulting you, get on rivals."
}

#sync safety
ready = False
guild = discord.Object(id=GUILD_ID)

#Tree Commands
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.tree.command(name="ask_aryan", description="Activate AI mode", guild = guild)
@app_commands.describe(question = "Say something: ")

async def ask_the_bum(interaction, question: str):
    await interaction.response.defer()
    question = question + ". Give a short, concise answer but be nice."
    reply = await call_gemini(question)
    await interaction.followup.send(reply)

@bot.event
async def on_ready():
    global ready
    if not ready:
        await bot.tree.sync() #clear global commands
        await bot.tree.sync(guild=guild)
        print(f"logged in as {bot.user} (id: {bot.user.id})")
        ready = True

@bot.tree.command(name = "hello", description = "say hello", guild=guild)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.name}!")
@bot.tree.command(name = "jared", description = "scottish man", guild=guild)
async def jared(interaction: discord.Interaction):
    await interaction.response.send_message("ew scottish man!")


@bot.event
async def on_message(message: discord.Message):
    #ignore messages from bot
    if message.author == bot.user:
        return
    content = message.content.lower()
    for keyword, response in RESPONSES.items():
        if keyword in content:
            await message.channel.send(response)
            break
if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("no DISCORD_TOKEN FOUND in environment")
    bot.run(TOKEN)
