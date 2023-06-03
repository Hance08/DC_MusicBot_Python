import discord
import asyncio
import yt_dlp as youtube_dl
from discord import app_commands
from discord import FFmpegPCMAudio
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
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

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:            
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)        
        return filename

class Music_Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="play" , with_app_command=True)
    async def play(self , ctx: commands.Context , *, query: str):
        if ctx.message.author.voice:
            music_channel = ctx.message.author.voice.channel
            await music_channel.connect()
            await ctx.send("機器人成功加入語音頻道 !")
        else:
            await ctx.send("你尚未在任何語音頻道 !")
        try:   
            server = ctx.message.guild
            music = server.voice_client            
            filename = await YTDSource.from_url(query)
            music.play(discord.FFmpegPCMAudio(executable=r"C:\FFmpeg\ffmpeg.exe" , source = filename))
            await ctx.send("--現在正在播放音樂--")
        except:
            await ctx.send("機器人尚未在任何語音頻道 !")
        
        while (True):
            if not music.is_paused():
                if not music.is_playing():                
                    break
            await asyncio.sleep(1)
    
        await music.disconnect()
        
    @commands.hybrid_command(name= 'leave', with_app_command= True)
    async def leave(self, ctx: commands.Context):
        if(ctx.voice_client):
           await ctx.guild.voice_client.disconnect()
           await ctx.send('機器人已離開語音頻道 !')
        else:
            await ctx.send('機器人不再語音頻道裡 !')
    
    @commands.hybrid_command(name= 'pasue', with_app_command= True)
    async def pause(self, ctx: commands.Context):
        music = ctx.voice_client        
        await music.pause()
        await ctx.send('音樂已暫停 !')
    
    @commands.hybrid_command(name='resume' , with_app_command=True)
    async def resume(self, ctx: commands.Context):
        music = ctx.voice_client
        await music.resume()
        await ctx.send("音樂繼續播放 !")
        
async def setup(bot):
    await bot.add_cog(Music_Player(bot))