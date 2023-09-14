import os
import discord
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector


from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")

SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")


intents = discord.Intents.all()
client = discord.Client(intents=intents)

sp_oauth = SpotifyOAuth(client_secret=SPOTIPY_CLIENT_SECRET)


sp = spotipy.Spotify(auth_manager=sp_oauth)

playlist_info = []

async def get_playlist_tracks(playlist_id, playlist_name, message_channel):
    
    database = mysql.connector.connect( 
    )
    mycursor = database.cursor()
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{playlist_name}` (song VARCHAR(255))"
    mycursor.execute(create_table_query)
    
    num_songs = 0
    results = sp.user_playlist_tracks("spotify", playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        song_name = track["track"]["name"]
        num_songs += 1

        sql = f"INSERT INTO `{playlist_name}` (song) VALUES (%s)"
        val = (song_name)
        mycursor.execute(sql, val)
        database.commit()
    await message_channel.send(f"{playlist_name} has been added to the database with {num_songs} songs")

    
    
    database.close()




