import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import random

#loading environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('TEST_ID'))
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
    "jared": "fud",
    "niamh": "Greatest Scottish woman of all time",
    "valorant": "Why don't we play rivals instead?",
    "rivals": "Best game ever btw",
    "emily": "Bug lady 🐞",
    "tash": "Group mum",
    "bekim": "Nazi",
    "aryan": "my master",
    "anyone on": "in other words 'someone play with me im lonely'",
    "fuck": "do you think swearing makes you cool?",
    "fucks": "do you think swearing makes you cool?",
    "shit": "do you think swearing makes you cool?",
    "piss": "do you think swearing makes you cool?",
    "cunt": "do you think swearing makes you cool?",
    "fud": "do you think swearing makes you cool?",
    "hi bot": "fuck off (sorry aryan makes me say that I actually love you guys :(",
    "sean": "the unc",
    "ava": "get on rivals.",
    "jeff": "That's me! :)"
}

NAMES = {
    "s.clifton": "Sean",
    "tishtash756": "Tash",
    "niamh02272": "Niamh",
    "jigglypuff0070": "Emily",
    "bekimthekid": "Bekim",
    "_wetbag": "Jared",
    "imaprettylittlerat": "Ava",
    "phxntom.27": "Aryan"
}

LIVE_VAL_HEROES = ["Gecko", "Killjoy", "Yoru", "Raze", "Clove", "Jett", "Sova", "Iso", "Viper", "Phoenix", "Breach", "Chamber", "Brimstone", "Cypher", "Deadlock", "Omen", "Neon", "Fade", "Harbor", "Skye", "Astra", "Vyse", "Kay-O", "Tejo", "Reyna", "Waylay", "Sage"]
FULL_VAL_HEROES = LIVE_VAL_HEROES.copy()

PISTOLS = ["classic", "shorty", "frenzy", "ghost", "sheriff"]
SMG = ["stinger", "spectre"]
SHOTGUNS = ["bucky", "judge"]
RIFLES = ["bulldog", "guardian", "phantom", "vandal"]
SNIPERS = ["marshall", "outlaw", "operator"]
LMG = ["ares", "odin"]

#sync safety
ready = False
guild = discord.Object(id=GUILD_ID)

#Tree Commands
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.tree.command(name="talk_to_landshark", description="Activate AI mode", guild=guild)
@app_commands.describe(question="Say something: ")
async def ask_jeff(interaction, question: str):
    await interaction.response.defer()
    question = question + ". Give a short, concise answer but be nice. Occasionally make a shark noise but don't do it after every message, something like 'mmrkk'"
    reply = await call_gemini(question)
    await interaction.followup.send(reply)

@bot.event
async def on_ready():
    global ready
    if not ready:
        await bot.tree.sync()
        await bot.tree.sync(guild=guild)
        print(f"logged in as {bot.user} (id: {bot.user.id})")
        ready = True

@bot.tree.command(name="hello", description="say hello", guild=guild)
async def hello(interaction: discord.Interaction):
    name = ""
    for username, fullName in NAMES.items():
        if username == interaction.user.name:
            name = fullName
    if name != "":
        await interaction.response.send_message(f"Hello {name}!")
    else:
        await interaction.response.send_message(f"Hello {interaction.user.name}!")

@bot.tree.command(name="jared", description="scottish man", guild=guild)
async def jared(interaction: discord.Interaction):
    await interaction.response.send_message("#1 Radiant")

#Mystery Wheel
@bot.tree.command(name="wheel_of_mythicality", description="Get a random Valorant hero", guild=guild)
async def hero_wheel(interaction: discord.Interaction):
    if LIVE_VAL_HEROES:
        num = random.randint(0, len(LIVE_VAL_HEROES) - 1)
        hero = LIVE_VAL_HEROES[num]
        name = ""
        gif_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTBzZTV4ZnZ2Njd4ZHN1bzl4d2NuNmJteGxiZHRrNmE1aG1pb2pnayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/U7LgoZb0E57QirLJ8F/giphy.gif"
        for username, fullName in NAMES.items():
            if username == interaction.user.name:
                name = fullName
        embed = discord.Embed(description=f"🎡 {name}, you are {hero}!")
        embed.set_image(url=gif_url)
        await interaction.response.send_message(embed=embed)
        LIVE_VAL_HEROES.remove(hero)
    else:
        await interaction.response.send_message("Gotta refresh the wheel 😔")

#Wheel refresh
@bot.tree.command(name="refresh_wheel", description="Refresh the wheel", guild=guild)
async def refresh_wheel(interaction: discord.Interaction):
    LIVE_VAL_HEROES[:] = FULL_VAL_HEROES
    await interaction.response.send_message("Mythicality refreshed")

#Random Gun assignment
@bot.tree.command(name="gun_game", description="Gives you a random selection of guns", guild=guild)
async def gun_game(interaction: discord.Interaction):
    num = random.randint(0, len(PISTOLS) - 1)
    firstGun = PISTOLS[num]
    num = random.randint(0, len(PISTOLS) - 1)
    gunTypeNum = random.randint(0, 5)

@bot.event
async def on_message(message: discord.Message):
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
