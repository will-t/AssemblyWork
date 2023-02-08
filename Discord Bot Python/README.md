This is a simple discord bot, using different python libraries.

You must have these depenencies to use the bot.

Python3
ffmpeg 
Youtubedl
yt-dlp
json
discord
discord.ext 
asyncio 
youtube search python
Video Search
openai

Aside from ffmpeg and youtubedl
these can be installed from the pip3 command
by finding them from the pypi website of addons
https://pypi.org/

For the usage of this bot, change the token in .env file to the token of your own bot through the discord creator portal
Then go into an change the name to the server you plan on using this in

After go to the directory that has the bot inside it, run python bot.py.

Usage commands in discord are listed in the bot file 

play songname 
queue songname //has a queue limit of three but this can easily be changed
stop
pause
resume
skip

This bot sends the content of the discord message to a youtube search, grabbes the link of the first most played video. 
Then it sends this link to a downloader and downloads at a high rate of speed grabbing the best quality link with the options listed. 
Then finally it will play the song over the voice feature of discord.ext by using the ffmpeg exe.



A new feature has been added,
prompt question

will ask the chat gpt ai a question of your choice
you must add the api key generated from their website to your file for this too work.