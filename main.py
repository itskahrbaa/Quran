import discord
from discord.ext import commands
from backend import Quran, Reciters

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="بوت بسيط للقرأن الكريم",
    intents=intents,
)

quran = Quran(bot)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    for guild in bot.guilds:
        await quran.radio_by_default(guild)

@bot.command()
async def play(ctx, recter: str):
    await quran.play(ctx, recter)

@bot.command()
async def playR(ctx, recter:str, sura:int):
    await quran.play_reciter(ctx, recter, sura)


bot.run("MTAxNDAzOTYxMjA3Njg2MzU2OA.G_hrUc.W7_HmPbrS9tkPdh8KyWVVw8yTbrmEXGqWjDgJI")