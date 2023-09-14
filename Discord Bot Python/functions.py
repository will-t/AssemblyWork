#This file contain the functions for the message commands
import mysql.connector
import random
from youtubesearchpython import VideosSearch
import discord
import asyncio
import yt_dlp


from ytdl import ydl_opts
queue = []

intents = discord.Intents.all()
client = discord.Client(intents=intents)

class MyMenu(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.add_item(discord.ui.Select(placeholder='Select a playlist!', min_values=1, max_values=1, options=options))

    @discord.ui.select()
    async def select(self, select, interaction):
        values = interaction.data.get('values')
        if values:
            await interaction.response.send_message(f'You selected {values[0]}!', ephemeral=True)
            try:
                database = mysql.connector.connect(
                )
                cursor = database.cursor()
                await play_playlist(values[0], self.message, cursor, database)
            except Exception as e:
                print(f"An error occurred: {e}")
                if database:
                    database.close()

class SimpleView(discord.ui.View):

    @discord.ui.button(label='Play', style=discord.ButtonStyle.green)
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await resume(self.message)

    @discord.ui.button(label='Pause', style=discord.ButtonStyle.blurple)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await pause(self.message)

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await stop(self.message)

    @discord.ui.button(label='Skip', style=discord.ButtonStyle.grey)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await skip_song(self.message)

async def button_function(message):
    view = SimpleView(timeout=300)
    message = await message.channel.send(view=view)
    view.message = message
    await view.wait()

async def help(message):
    message1 = ['play: Plays a song. Usage: play <song name or youtube link>',
    'skip: Skips the current song. Usage: skip',
    'stop: Stops the current song. Usage: stop',
    'resume: Resumes the current song. Usage: resume',
    'pause: Pauses the current song. Usage: pause',
    'playlist: Displays all playlists and gives an option to start a playlist or to edit a playlist. Usage: playlist',
    'randomplaylist: Plays a random playlist. Usage: randomplaylist',
    'listplaylist: Lists all playlists. Usage: listplaylist',
    'CreateNewServer: Creates a new server. Usage: CreateNewServer',
    'prompt: Uses OpenAI to generate text. Usage: prompt <command/question>',
    'spotifylink: Gets the songs in a Spotify playlist. Usage: spotifylink <playlist link>',
    'playlistmenu: Select a playlist to play. Usage: playlistmenu',
    'leave: Bot leaves the voice channel. Usage: leave',
    'join: Bot joins the voice channel. Usage: join']
    chunk = ""
    for i in message1:
        chunk += i + "\n"
    await message.channel.send(f"```{chunk}```")
async def leave_voice(message):
    voice_client = message.voice_client
    if voice_client:
        voice_client.disconnect()
    else:
        await message.send("The bot is not connected to a voice channel.")
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

async def queue_play(message, url):
    if (len(queue) < 8):
        queue.append(url)
        await message.channel.send("Song added to queue")
    else:
        await message.channel.send("Queue is full")
async def show_quene(message):
    if (len(queue) == 0):
        await message.channel.send("Queue is empty")
    else:
        await message.channel.send("Queue:")
        for x in queue:
            await message.channel.send(x)

async def join_voice(message):
    voice_state = message.author.voice
    if not voice_state or not voice_state.channel:
        await message.channel.send("You're not in a voice channel!")
        return
    voice_channel = voice_state.channel
    if not message.guild.voice_client:
        await voice_channel.connect()
    else:
        await message.guild.voice_client.move_to(voice_channel)

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
        await button_function(message)
        
    if len(queue) > 0:
        next_song_url = queue.pop(0)
        await start_song(message, next_song_url)
    else:
        await message.channel.send("Finished with queue")

async def playlistStart(message):
    try:
            database = mysql.connector.connect(
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
                                    sql = ("INSERT INTO "+x.content+" (song) VALUES ('"+a.content+"')")#reference
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
    
async def randomSong(message):
    try:
            database = mysql.connector.connect(
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

async def listPlaylist(message):
    try:
            database = mysql.connector.connect(
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

def playlistmenu():
    try:
        database = mysql.connector.connect(
        )
        cursor = database.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        playlists = [table[0] for table in tables]
        database.close()
        return playlists
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

async def play_playlist(playlist, message, cursor, database):
    await message.channel.send("Starting playlist")
    sql = (f"SELECT song FROM {playlist}")
    cursor.execute(sql)
    songs = cursor.fetchall()
    for song in songs:
        regStr = ""
        for char in song:
            regStr += char
        await message.channel.send(f"Now playing: {regStr}")
        videoSearch = VideosSearch(regStr, limit=1)
        url = videoSearch.result()['result'][0]['link']
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.channel.send("You're not in a voice channel!")
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
    database.close()

