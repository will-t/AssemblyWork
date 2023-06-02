# bot.py
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
import youtube_dl
import os
import openai
import random
import subprocess
from youtubesearchpython import VideosSearch
import discord
import yt_dlp
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
from discord.ext import commands, tasks
import youtube_dl
import asyncio
import mysql.connector
load_dotenv()

TOKEN='OTQxNzI3ODUyNDYwNjY2OTAx.GSvUxN.t5MMqQPENXLWGqJPMnbtoEvnIhkeC4eumwXQjE'
GUILD="JMAN's Dictatorship"
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
queue = []
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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

ytdl = youtube_dl.YoutubeDL(ydl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, **ffmpeg_options)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return cls(filename, data=data)
    
class SimpleView(discord.ui.View):
    
    #var : bool = None

    #async def disable_buttons(self):
    #    for item in self.children:
    #        item.disabled = True
    #        await self.message.edit(view=self)

    #async def on_timeout(self):
    #    await self.message.channel.send("Timed out")
    #    await self.disable_buttons()

    @discord.ui.button(label='Play', style=discord.ButtonStyle.green)
    async def play1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await resume(self.message)



        #self.var = True
        

    @discord.ui.button(label='Pause', style=discord.ButtonStyle.blurple)
    async def pause1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await pause(self.message)
        #self.var = True
        
        

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
    async def stop1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await stop(self.message)

        #self.var = False

    @discord.ui.button(label='Skip', style=discord.ButtonStyle.grey)
    async def skip1(self, interaction: discord.Interaction, button: discord.ui.Button):
            await skip_song(self.message)
        #self.var = False
        


async def button(message):

    view = SimpleView(timeout=300)
    
    message = await message.channel.send(view=view)
    view.message = message
    await view.wait()
    #await view.disable_buttons()
    
    #if view.var is None:
    #    print("Timeout")

    #elif view.var is True:
    #    print("OK")

    #elif view.var is False:
    #    print("Cancel")

#@bot.command(name='!commands', help='Shows all commands')
async def show_commands(message):
    await message.send('Commands: !s, !stop, !pause, !resume, !skip, !queue')

async def leave_voice(message):
    voice_client = message.voice_client
    if voice_client:
        voice_client.disconnect()
    else:
        await message.send("The bot is not connected to a voice channel.")

#@bot.command(name='!skip', help='Skips the current song in the queue')
async def skip_song(message):
    voice_client = message.voice_client
    if not voice_client:
        await message.send("The bot is not connected to a voice channel.")
        return
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await message.send('No items left in queue')

async def stop(message):
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await message.channel.send("The bot is not playing anything at the moment.")
async def start_song(message, url):
    server = message.guild
    voice_channel = server.voice_client
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        sanitized_info = ydl.sanitize_info(info)
        filename = ydl.prepare_filename(sanitized_info)
    print(filename)
    audio_source = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
    voice_channel.play(audio_source)
    while voice_channel.is_playing():
        await asyncio.sleep(1)
        #create instance of bot button view/ await for response, length as long as song length
        #after song finishes terminate button view and continue next song 
        await button(message)
        
    if len(queue) > 0:
        next_song_url = queue.pop(0)
        await start_song(message, next_song_url)
    else:
        await message.channel.send("Finished with queue")
async def queue_play(message, url):
    if (len(queue) < 8):
        queue.append(url)
        await message.channel.send("Song added to queue")
    else:
        await message.channel.send("Queue is full")
async def resume(message):
    voice_client = message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await message.channel.send("The bot was not playing anything before this. Use play_song command")        
async def pause(message):
    voice_client = message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await message.channel.send("The bot is not playing anything at the moment.")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('play') and message.content != 'playlist':
            print (message.author.id)
            voice_state = message.author.voice
            if not voice_state or not voice_state.channel:
                await message.channel.send("You're not in a voice channel!")
                return
            voice_state = message.author.voice
            if not voice_state:
                await message.channel.send(f'{message.author.mention} is not connected to a voice channel')
                return
            voice_channel = voice_state.channel
            if not message.guild.voice_client:
                await voice_channel.connect()
            else:
                await message.guild.voice_client.move_to(voice_channel)
            search = message.content[5:]
            try:
                database = mysql.connector.connect(
                host="localhost",
                user="music1",
                password="Ocea6nic1+",
                database="random"
            )
                cursor = database.cursor()
                sql = ("INSERT INTO random (song) VALUES ('"+search+"')")
                cursor.execute(sql)
                database.commit()
                database.close()
            except:
                await message.channel.send("Error adding to random database")
            videoSearch = VideosSearch(search, limit=1)
            url = videoSearch.result()['result'][0]['link']
            voice_client = message.guild.voice_client
            if voice_client.is_playing():
                await queue_play(message, url)
            await start_song(message, url)
            return
    if message.content.startswith('leave'):
        await message.guild.voice_client.disconnect()
        return
    if message.content == "randomplaylist":
        try:
            await randomSong(message)
        except:
            await message.channel.send("Error playing random song")
        return
    if message.content == 'playlist':   
        try:
            await playlistStart(message)
        except:
            await message.channel.send("Error: Function did not Complete")
        return
    if message.content == 'listplaylists':
        try:
            await listPlaylist(message)
        except:
            await message.channel.send("Error: Function did not Complete")
        return
    if message.content.startswith('skip'):
        await skip_song(message)
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
    if message.content.startswith('CreateNewServer'):
        await message.channel.send('Creating New Server')
        proc = subprocess.Popen(['/bin/bash', '/home/user/Send/testing.sh'], stdout=subprocess.PIPE)
        while True:
            msg = await client.wait_for('message')
            if msg.content == 'stopserver':
                proc.terminate()
                await message.channel.send('Server stopped.')
                break
    if message.content.startswith('clean') :
        if message.author.id == 286242966413246464:
            try:
                subprocess.Popen(['/bin/bash', '/home/user/Send/clear.sh'], stdout=subprocess.PIPE)
                await message.channel.send('Cleaned up files')
            except:
                await message.channel.send('Error cleaning up files')
            return
        else:
            await message.channel.send('You are not allowed to use this command')
            return
    if message.content == 'sshon':
        if message.author.id == 286242966413246464:
            try:
                subprocess.Popen(['/bin/bash', '/home/user/Send/sshenable.sh'], stdout=subprocess.PIPE)
                await message.channel.send("Flipped SSH")
                return
            except:
                await message.channel.send("Error flipping SSH")
                return
    if message.content == 'sshoff':
        if message.author.id == 286242966413246464:
            try:
                subprocess.Popen(['/bin/bash', '/home/user/Send/sshdisable.sh'], stdout=subprocess.PIPE)
                await message.channel.send("Flipped SSH")
                return
            except:
                await message.channel.send("Error flipping SSH")
                return
    if message.content.startswith('override'):
        url = message.content[9:]
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.channel.send("You're not in a voice channel!")
            return
        voice_state = message.author.voice
        if not voice_state:
            await message.channel.send(f'{message.author.mention} is not connected to a voice channel')
            return
        voice_channel = voice_state.channel
        if not message.guild.voice_client:
            await voice_channel.connect()
        else:
            await message.guild.voice_client.move_to(voice_channel)
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            await queue_play(message, url)
        await start_song(message, url)
        await message.content.send('Song override complete')
        return
    if message.content.startswith('prompt'):
        openai.api_key = ''
        x = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.content[7:],
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        await message.channel.send(x.choices[0].text)
        return
    if message.content.startswith('leave'):
        await leave_voice(message)
        return
    #await client.process_commands(message)

async def on_ready(ctx):
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
async def listPlaylist(message):
    try:
            database = mysql.connector.connect(
                host="localhost",
                user="music1",
                password="Ocea6nic1+",
                database="random"
            )
            cursor = database.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            regStr = ""
            for table in tables:
                x = 1 
                regStr += "Playlist:" + str(x) + " "
                for char in table:
                    regStr += char
                x += 1
                regStr += "\n"
            await message.channel.send(regStr)
            database.close()
    except:
            await message.channel.send("Error: Could not connect to database")
    return
async def randomSong(message):
    try:
            database = mysql.connector.connect(
                host="localhost",
                user="music1",
                password="Ocea6nic1+",
                database="random"
            )
            cursor = database.cursor()
            try:
                cursor.execute("use random")
                cursor.execute("SELECT * FROM random")
                songs = cursor.fetchall()
                for table in songs:
                    regStr = ""
                    for char in table:
                        regStr += char
                    strArr = strArr.pushback(regStr)
                x = len(strArr)
                while x > 0: 
                    y = random.randint(0, x)
                    videoSearch = VideosSearch(strArr[y], limit = 1)
                    url = videoSearch.result()['result'][0]['link']
                    voice_state = message.author.voice
                    if not voice_state or not voice_state.channel:
                        await message.channel.send("You're not in a voice channel!")
                        return
                    voice_state = message.author.voice
                    if not voice_state:
                        await message.channel.send(f'{message.author.mention} is not connected to a voice channel')
                        return
                    voice_channel = voice_state.channel
                    if not message.guild.voice_client:
                        await voice_channel.connect()
                    else:
                        await message.guild.voice_client.move_to(voice_channel)
                    voice_client = message.guild.voice_client
                    if voice_client.is_playing():
                        await queue_play(message, url)
                    await start_song(message, url)
                    strArr.pop(y)
                    x -= 1
                database.close()
                return
            except:
                await message.channel.send("Error: Problem with random playlist database")
                return
    except:
        await message.channel.send("Error: Connecting to database")
        return
async def playlistStart(message):
    try:
            database = mysql.connector.connect(
                host="localhost",
                user="music1",
                password="Ocea6nic1+",
                database="random"
            )
            cursor = database.cursor()
            try:
                await message.channel.send("Please select a playlist")
                await listPlaylist(message)
                x = await client.wait_for('message')
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    regStr = ""
                    for char in table:
                        regStr += char
                    if(x.content == regStr):
                        await message.channel.send("Would you like to edit the playlist?")
                        y = await client.wait_for('message')
                        if y.content == "Y" or y.content == "y" or y.content == "yes":
                            await message.channel.send("Would you like to add or remove songs?")
                            z = await client.wait_for('message')
                            if z.content == "add":
                                while True:
                                    await message.channel.send("Enter a song to add, when finished type done:")
                                    a = await client.wait_for('message')
                                    if a.content == "done":
                                        return
                                    sql = ("INSERT INTO "+x.content+" (song) VALUES ('"+a.content+"')")
                                    cursor.execute(sql)
                                    database.commit()
                                    await message.channel.send("Song added to playlist")
                                return
                            if z.content == "remove":
                                sql = ("SELECT song FROM "+x.content)
                                cursor.execute(sql)
                                songs = cursor.fetchall()
                                regStr = ""
                                for song in songs:
                                    for char in song:
                                        regStr += char
                                    regStr += "\n"
                                await message.channel.send(regStr)
                                while True:
                                    await message.channel.send("Enter a song to remove, when finished type done:")
                                    a = await client.wait_for('message')
                                    if a.content == "done":
                                        return
                                    sql = ("DELETE FROM "+x.content+" WHERE song = '"+a.content+"'")
                                    cursor.execute(sql)
                                    database.commit()
                                    await message.channel.send("Song "+a.content+" removed from playlist")
                                return
                        if y.content == "N" or y.content == "n" or y.content == "no":
                            await message.channel.send("Starting playlist")
                            sql = ("SELECT song FROM "+x.content)
                            cursor.execute(sql)
                            songs = cursor.fetchall()
                            for song in songs:
                                regStr = ""
                                for char in song:
                                    regStr += char
                                await message.channel.send("Now playing: "+regStr)
                                videoSearch = VideosSearch(regStr, limit=1)
                                url = videoSearch.result()['result'][0]['link']
                                voice_state = message.author.voice
                                if not voice_state or not voice_state.channel:
                                    await message.channel.send("You're not in a voice channel!")
                                    return
                                voice_state = message.author.voice
                                if not voice_state:
                                    await message.channel.send(f'{message.author.mention} is not connected to a voice channel')
                                    return
                                voice_channel = voice_state.channel
                                if not message.guild.voice_client:
                                    await voice_channel.connect()
                                else:
                                    await message.guild.voice_client.move_to(voice_channel)
                                voice_client = message.guild.voice_client
                                if voice_client.is_playing():
                                    await queue_play(y, url)
                                await start_song(y, url)
                            database.close()
                            return
                cursor.execute("CREATE TABLE " + x.content + "(song VARCHAR(45))")
                await message.channel.send("Playlist Created")
                await message.channel.send("Would you like to add songs to the playlist?")
                y = await client.wait_for('message')
                if y.content == "Y" or y.content == "y" or y.content == "yes":
                    await message.channel.send("Add songs, when you are finished type done")
                    while True:
                        z = await client.wait_for('message')
                        if z.content == "done":
                            await message.channel.send("Songs added to playlist")
                            return
                        else:
                            sql = ("INSERT INTO "+x.content+" (song) VALUES ('"+z.content+"')")
                            cursor.execute(sql)
                            await message.channel.send("Song added to playlist")
                            database.commit()
                else:
                    return
            except:
                await message.channel.send("Error: Problem with playlist database")
                y = await client.wait_for('message')
                if y.content == "Y" or y.content == "y" or y.content == "yes": 
                    return
                else:
                    return
    except:
        await message.channel.send("Error: Connecting to database")
        return
if __name__ == "__main__" :
    client.run(TOKEN)
