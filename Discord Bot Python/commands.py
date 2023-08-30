#This file contain the functions for the message commands
import mysql.connector
import random
from youtubesearchpython import VideosSearch
import discord
import asyncio
import yt_dlp
import button
from ytdl import ydl_opts
queue = []

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)



async def help(message):
    await message.send('Commands: !s, !stop, !pause, !resume, !skip, !queue')
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
        #create instance of bot button view/ await for response, length as long as song length
        #after song finishes terminate button view and continue next song 
        await button_function(message)
        
    if len(queue) > 0:
        next_song_url = queue.pop(0)
        await start_song(message, next_song_url)
    else:
        await message.channel.send("Finished with queue")