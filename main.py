import discord
from discord.ext import commands
from backend import quran


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="بوت بسيط للقرأن الكريم",
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    for guild in bot.guilds:
        await quran(bot).Radio(guild)


bot.run("عيب متبصش")
