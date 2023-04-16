from unittest import result
import discord
from discord.ext import commands
import json
import requests
from difflib import get_close_matches


# TODO هعمل ان البيانات القراء وكل شئ تتحمل علي الجهاز ومتتمسحش في حال اختار الشخص يمسحه 
# TODO + هعمل امر تحديث في لوحة CMD لو اتعملت او من اوامر البوت ذات نفسه
# TODO لتسريع العمليه وتسهيل استهلاك الماموري واستخدام مساحه الجهاز عوضٌ عن الميمور
# TODO وأخراج اقصي سرعه ممكنة للبوت

class Data():
    def __init__(self):
        """ بيانات السيرفرات وأعداداتها `تفحص` , `وتعدل` هنا !"""
        self.defaultdata: dict = json.load(open("data.json", encoding='utf-8'))

    def check(self, guild: discord.Guild):
        """ JSON وظيفة الـ `فحص` اذا كان يوجد سيرفر جديد ام لاء من هنا وتحفظ في """
        if str(guild.id) in self.defaultdata.keys():
            return self.defaultdata[str(guild.id)]
        else:
            self.defaultdata.update({ str(guild.id):{ "volume":1, "staychannel":{"status":False,"channelID":"id"}, "radio":"https://Qurango.net/radio/tarateel"} })
            with open("data.json", "w") as data:
                json.dump(self.defaultdata, data, indent=4)
            return self.defaultdata[str(guild.id)]

    def update(self, ctx: commands.Context, volume: float = None, stayChannel:bool = None, channelId:str = None, radio:str = None):
        """ Json وظيفة الـ `تعديل` علي اي معلومة داخل """
        text = ""
        try:
            guild = self.defaultdata[str(ctx.guild.id)]
        except:
            self.check(guild)
        if volume and volume <= 150:
            # لن يعمل في حال كانت القيمة اكتر من 150
            guild["volume"] = volume
            if guild["volume"] < volume:
                text = "رفع صوت البوت"
            else:
                text = "رفع صوت البوت"
        elif stayChannel:
            guild["staychannel"]["status"] = stayChannel
            if guild["staychannel"]["status"]:
                text = "خاصية التثبيت تعمل"
            else:
                text = "خاصية التثبيت متوقفه"
        elif channelId:
            if guild["staychannel"]["channelID"] == channelId:
                text = "يبدو انك لمتضف شئ جديد"
            else:
                guild["staychannel"]["channelID"] = channelId
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

class Quran():
    def __init__(self, bot_:commands.Bot):
        self.bot = bot_
            
    async def radio_by_default(self, guild : discord.Guild): 
        data_ = Data().check(guild)
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

    async def play_url(self, ctx: commands.Context, reciter: str):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(reciter))
        ctx.guild.voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)

    async def play_reciter(self, ctx: commands.Context, reciter:str, sura:int, arabic: bool = True):
        if arabic:
            reciters = Reciters.get_reciters()[0]
        else:
            reciters = Reciters.get_reciters()[1]
        result = get_close_matches(reciter, reciters, cutoff=0.5)  
        reciterinfo = reciters[result[0]]
        url = reciterinfo["server"]+"/"+'{:03}'.format(sura)+".mp3"
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
        ctx.guild.voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)
        await ctx.send(url)

        

    # ==========================
    # TODO : مسودة
    # ==========================
    # def currentData(self, context: commands.Context, args):
    #     """يسحب البيانات الخاصة بالقارئ الذي يعمل في الخلفية `الصوت` و `رابط القارئ` و `ايدي الغرفة الصوتية`"""
    #     changes = {"guild":str(context.guild.id)}
    #     voice = context.voice_client
    #     for value in args:
    #         match value:
    #             case 'volume':
    #                 changes.update({'volume':voice.source.volume})
    #             case 'channel':
    #                 changes.update({'channel':str(voice.channel.id)})
    #             case 'recter':
    #                 changes.update({'recter':voice.source.original._process.args[2]})
    #     return changes

    
    # class Dropdown(discord.ui.Select):
    #     def __init__(self, ctx: commands.Context, bot_: discord.Bot):
    #         self.bot = bot_
    #         self.defaultdata: dict = json.load(open("data.json", encoding='utf-8'))

    #         options = [
    #             discord.SelectOption(label="Recter", description="قناة القارئ التي تريدها", emoji="📻", value="recter"),
    #             discord.SelectOption(label="Channel", description="الغرفة الصوتية الأفتراضيه", emoji="📞", value="channel"),
    #             discord.SelectOption(label="Volume", description="صوت البوت", emoji="🔊", value="volume"),
    #         ]

    #         super().__init__(
    #             placeholder="ماذا تريد حفظ من الاعدادت الحاليه",
    #             min_values=1,
    #             max_values=3,
    #             options=options,
    #         )
    #         self.values_ = quran(self.bot).currentData(ctx, self.values)
    #     async def callback(self, interaction: discord.Interaction):
    #         guildData: dict = Data().check(interaction.guild)
    #         for key , value in self.values_.items():
    #             match key:
    #                 case 'volume':
    #                     guildData.update({'volume':value})
    #                 case 'channel':
    #                     guildData["staychannel"].update({'channelID':value})
    #                 case 'recter':
    #                     guildData.update({'radio':value})
    #             with open('data.json', 'w', encoding='utf-8') as f:
    #                 json.dump(guildData, f, indent=4)
    #         await interaction.response.send_message(f"{key}: {value} !!")

class Reciters:
    def __init__(self):
        pass
        
    def get_radio(self):
        """Returns dict with `name` and `radio_url`"""
        res = requests.get('https://api.mp3quran.net/radios/radio_arabic.json')
        response: dict = json.loads(res.text)
        return response["radios"]

    def to_list(self, list: dict): return [ reciter for reciter in list.keys()]
    
    def get_reciters(): # هيتسمح عند التحديث ! الجديد 
        res = requests.get('https://api.mp3quran.net/reciters/_arabic.json')
        resE = requests.get('https://api.mp3quran.net/reciters/_english.json')
        response = json.loads(res.text)
        responseE = json.loads(resE.text)
        reciters = {}
        recitersE = {}
        for i in response["reciters"]:
            reciters.update({
            i["name"]: {"name":i["name"], "id":i['id'], "server":i['Server'], "rewaya":i['rewaya'], "count":i['count'], "letter":i['letter'], "suras":i['suras']}})
        for i in responseE["reciters"]:
            recitersE.update({
            i["name"]: {"name":i["name"], "id":i['id'], "server":i['Server'], "rewaya":i['rewaya'], "count":i['count'], "letter":i['letter'], "suras":i['suras']}})
        return (reciters,recitersE)