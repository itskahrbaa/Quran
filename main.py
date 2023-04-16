import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from backend import Quran, Reciters
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="بوت بسيط للقرأن الكريم",
    intents=intents,
)


quran = Quran(bot)
token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    for guild in bot.guilds:
        await quran.radio_by_default(guild)


@bot.command()
async def play(ctx, recter: str):
    await quran.play_url(ctx, recter)

@bot.command()
async def playR(ctx, recter:str, sura:int):
    await quran.play_reciter(ctx, recter, sura)

@bot.command()
async def play_s(ctx, recter:str, sura:int):
    await quran.play_reciter(ctx, recter, sura, arabic=False)


bot.run(token)