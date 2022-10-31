# bot.py
import cgi
import os
from youtubesearchpython import VideosSearch
import discord
import json
import yt_dlp
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
from discord.ext import commands, tasks
import youtube_dl
import asyncio
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}  
load_dotenv()
TOKEN = os.getenv('SECRET_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
guild = os.getenv('DISCORD_GUILD')
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)
queue = []
ydl_opts = {}
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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
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
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.command(name='commands', help='Shows all commands')
async def commands(ctx):
    await ctx.send('Commands= !s, !stop, !pause, !resume, !skip, !queue'.format(ctx.message.author.name))

@bot.event
async def leave(message):
    voice_client = message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await message.channel.send("The bot is not connected to a voice channel.")
@bot.event
async def join(message):
    if not message.author.voice:
        await message.send("{} is not connected to a voice channel".format(message.author.name))
        return
    else:
        channel = message.author.voice.channel
    #check if bot is already in a voice channel
    if message.guild.voice_client:
        return 
    else:
        await channel.connect()

@bot.event
async def start_song(message, url):
    server = message.guild
    voice_channel = server.voice_client
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        json.dumps(ydl.sanitize_info(info))
        filename = ydl.prepare_filename(info)
    print(filename)
    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
    await message.channel.send('**Now playing:** {}'.format(filename)) 
    while True:
        if voice_channel.is_playing():
            await asyncio.sleep(1)
            print("waiting currently")
        else:
            if len(queue) > 0:
                url = queue.pop(0)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    json.dumps(ydl.sanitize_info(info))
                    filename = ydl.prepare_filename(info)
                print(filename)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
                await message.channel.send('**Now playing:** {}'.format(filename))
                print("Song should started playing by now")
            else:
                await message.channel.send("King of Cum is finished with queue")
                break
@bot.event
async def skip(message):
    voice_channel = message.guild.voice_client
    if voice_channel.is_playing():
        await voice_channel.stop()
        if(len(queue) > 0):
            url = queue.pop(0)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                json.dumps(ydl.sanitize_info(info))
                filename = ydl.prepare_filename(info)
            print(filename)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await message.channel.send('**Now playing:** {}'.format(filename))
            print("Song should started playing by now")
        else:
            await message.channel.send('No items left currently in the queue')
@bot.event
async def pause(message):
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await message.channel.send("The bot is not playing anything at the moment.")
    
@bot.event
async def resume(message):
    voice_client = message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await message.channel.send("The bot was not playing anything before this. Use play_song command")
@bot.event
async def stop(message):
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await message.channel.send("The bot is not playing anything at the moment.")
@bot.event
async def queue_play(message, url):
    if (len(queue) < 3):
        queue.append(url)
        await message.channel.send("Song added to queue")
    else:
        await message.channel.send("Queue is full")
@bot.event
async def on_message(message):
    if message.content.startswith('play'):
        search = message.content.lower()
        videoSearch = VideosSearch(search, limit=1)
        url = videoSearch.result()['result'][0]['link']
        await join(message)
        await message.channel.send('Downloading song')
        await start_song(message, url)
        await print (url)
        return
    if message.content.startswith('leave'):
        await message.guild.voice_client.disconnect()
        return
    if message.content.startswith('skip'):
        await skip(message)
        return
    if message.content.startswith('pause'):
        await pause(message)
        return
    if message.content.startswith('resume'):
        await resume(message)
        return
    if message.content.startswith('stop'):
        await stop(message)
        return    
    if message.content.startswith('queue'):
        search = message.content.lower()
        videoSearch = VideosSearch(search, limit=1)
        url = videoSearch.result()['result'][0]['link']
        await queue_play(message, url)
        await print (url)
        return
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
if __name__ == "__main__" :
    bot.run(TOKEN)
