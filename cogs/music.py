import discord #匯入模組
import asyncio #匯入模組
import yt_dlp as youtube_dl #匯入模組
from discord import app_commands #匯入模組
from discord import FFmpegPCMAudio #匯入模組
from discord.ext import commands #匯入模組

youtube_dl.utils.bug_reports_message = lambda: '' #設置 youtube_dl 的 bug_reports_message 為空函式

ytdl_format_options = { #ytdl的設定格式
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = { #ffmpeg的設定格式
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options) # 創建 YoutubeDL 物件

#建立 YTDSource類別
class YTDSource(discord.PCMVolumeTransformer):
    #初始化方法
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)# 呼叫父類別 discord.PCMVolumeTransformer 的初始化方法，以便設定音量轉換器的屬性
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod #類別方法 from_url
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop() #首先檢查是否提供了事件迴圈，如果沒有則使用 asyncio.get_event_loop() 獲取當前事件迴圈
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)) #使用 loop.run_in_executor() 方法在另一個執行緒中執行 ytdl.extract_info()，這樣可以避免阻塞事件迴圈
        #檢查 data 中是否有多個項目（通常是在播放清單中），如果有，我們只保留第一個項目
        if 'entries' in data:            
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data) #我們根據 stream 參數的值來決定返回的檔案名稱，如果是以串流方式下載，則使用音訊資料的標題作為檔案名稱，否則使用 ytdl.prepare_filename() 方法來準備檔案名稱       
        return filename

class Music_Player(commands.Cog):
    #初始化方法
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="play" , with_app_command=True) #設定斜線指令名稱為play
    async def play(self , ctx: commands.Context , *, query: str):
        if ctx.message.author.voice: #檢查機器人是否在語音頻道
            music_channel = ctx.message.author.voice.channel
            await music_channel.connect() #連線至輸入指令者的語音頻道
            await ctx.send("機器人成功加入語音頻道 !")
        else:
            await ctx.send("你尚未在任何語音頻道 !") #若輸入指令者未加入語音頻道則會顯示
        try:   
            server = ctx.message.guild
            music = server.voice_client            
            filename = await YTDSource.from_url(query) #使用 YTDSource 類別的 from_url 方法從指定的 query URL 中獲取音樂的檔案名稱
            music.play(discord.FFmpegPCMAudio(executable=r"C:\FFmpeg\ffmpeg.exe" , source = filename)) #使用 discord.FFmpegPCMAudio 類別來播放音樂播放音樂
            await ctx.send("--現在正在播放音樂--")
        except:
            await ctx.send("機器人尚未在任何語音頻道 !")
            
        #當音樂播放完時，自動退出語音頻道     
        while (True): 
            if not music.is_paused() and not music.is_playing(): #檢查是否為暫停 是否正在播放                
                    break #若沒暫停也沒在播放則跳出迴圈
            await asyncio.sleep(1) #休一秒然後再次執行迴圈
    
        await music.disconnect() #退出
        
    @commands.hybrid_command(name= 'leave', with_app_command= True) #設定斜線指令名稱為leave
    async def leave(self, ctx: commands.Context):
        if(ctx.voice_client): #檢查機器人是否在語音頻道
           await ctx.guild.voice_client.disconnect() #退出
           await ctx.send('機器人已離開語音頻道 !') #顯示退出訊息
        else:
            await ctx.send('機器人不再語音頻道裡 !') #當機器人未在語音頻道時卻使用此指令則顯示訊息
    
    @commands.hybrid_command(name= 'pasue', with_app_command= True) #設定斜線指令名稱為pause
    async def pause(self, ctx: commands.Context):
        music = ctx.voice_client 
        if(music): #檢查機器人是否在語音頻道              
            await music.pause() #暫停
            await ctx.send('音樂已暫停 !') #顯示暫停訊息
        else:
            await ctx.send('機器人不再語音頻道裡 !') #當機器人未在語音頻道時卻使用此指令則顯示訊息
    
    @commands.hybrid_command(name='resume' , with_app_command=True)
    async def resume(self, ctx: commands.Context):
        music = ctx.voice_client 
        if(music): #檢查機器人是否在語音頻道              
            await music.resume() #繼續
            await ctx.send('音樂繼續播放 !') #顯示繼續訊息
        else:
            await ctx.send('機器人不再語音頻道裡 !') #當機器人未在語音頻道時卻使用此指令則顯示訊息
        
async def setup(bot):
    await bot.add_cog(Music_Player(bot)) #設定機器人（bot）並將 Music_Player 類別的實例作為一個 "cog"（插件）添加到機器人中。