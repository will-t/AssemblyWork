#This file contain the message commands
import os
from dotenv import load_dotenv
import os
import openai
import subprocess
import discord
from dotenv import load_dotenv
import mysql.connector
from youtubesearchpython import VideosSearch
from commands import resume, pause, stop, skip_song, randomSong, playlistStart, listPlaylist, join_voice, leave_voice, queue_play, help, start_song
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
openai.api_key = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)


 
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
        response = openai.Completion.create(
        model="gpt-4",
        prompt=message.content[7:],
        max_tokens=1000
        )
        await message.channel.send(response.choices[0].text)
        return
    if message.content.startswith('leave'):
        await leave_voice(message)
        return
    if message.content.startswith('join'):
        await join_voice(message)
        return
    if message.content.startswith('help'):
        await help(message)
        return

async def on_ready(ctx):
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


if __name__ == "__main__" :
    client.run(TOKEN)
