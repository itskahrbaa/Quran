from cgitb import text
import discord
from discord.ext import commands
import json

class data():
    def __init__(self):
        """ بيانات السيرفرات وأعداداتها `تفحص` , `وتعدل` هنا !"""
        self.defaultData: dict = json.load(open("data.json", encoding='utf-8'))

    def check(self, guild: discord.Guild):
        """ JSON وظيفة الـ `فحص` اذا كان يوجد سيرفر جديد ام لاء من هنا وتحفظ في """
        if str(guild.id) in self.defaultData.keys():
            return self.defaultData[str(guild.id)]
        else:
            self.defaultData.update({ str(guild.id):{ "volume":1.0, "staychannel":{"status":False,"channelID":"id"}, "radio":"https://Qurango.net/radio/tarateel"} })
            with open("data.json", "w") as data:
                json.dump(self.defaultData, data, indent=4)
            return self.defaultData[str(guild.id)]

    def update(self, ctx: discord.ApplicationContext, volume: float = None, stayChannel:bool = None, channelId:str = None, radio:str = None):
        """ Json وظيفة الـ `تعديل` علي اي معلومة داخل """
        text = ""
        try:
            guild = self.defaultData[str(ctx.guild.id)]
        except:
            self.check(guild)
        if volume:
            guild["volume"] = volume
            if guild["volume"] < volume:
                text = "رفع صوت البوت"
            else:
                text = "رفع صوت البوت"
        elif stayChannel:
            guild["status"] = stayChannel
            if guild["status"]:
                text = "خاصية التثبيت تعمل"
            else:
                text = "خاصية التثبيت متوقفه"
        elif channelId:
            if guild["channelID"] == channelId:
                text = "يبدو انك لمتضف شئ جديد"
            else:
                guild["channelID"] = channelId
                text = "تم اضافة غرفة جديد"
        elif radio:
            if guild["radio"] == radio:
                text = "انه بالفعل نفس القناة القديمة"
            else:
                guild["radio"] = radio
                text = "تم اضافة قناة راديو جديدة"
        else:
            raise Exception("يبدو ان هناك خطا !")
        return text

class quran():
    def __init__(self, bot_:commands.Bot):
        self.bot = bot_
            
    async def Radio(self, guild : discord.Guild):
        data_ = data().check(guild)
        # ---------- Var
        staychannel = data_["staychannel"]
        radioURL = data_["radio"]
        volume = data_["volume"]
        # ----------------------
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(radioURL), volume=volume)
        try:
            if staychannel["status"]:
                channel = await guild.fetch_channel(int(staychannel["channelID"]))
                await channel.connect()
            else:
                return
        except:
            return
        guild.voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)

