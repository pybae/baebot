from discord.ext import commands
import discord
from discord import opus
from discord import FFmpegOpusAudio
from music import search_songs
import ctypes
import os

token = os.getenv('BAEBOT_TOKEN')
if token:
    print("Initializing baebot with token: " + token)
else:
    print("No BAEBOT_TOKEN found. Set BAEBOT_TOKEN and retry")
    sys.exit()

voice_client = None
bot = commands.Bot(command_prefix='$')

discord.opus.load_opus("libopus.so.0")
print(discord.opus.is_loaded())

@bot.command()
async def play(ctx, arg):
    voice_channel = bot.get_channel(570805084087255071)
    voice_client = await voice_channel.connect()
    (song, artist, file_path) = search_songs(arg)
    await ctx.send('Now playing {} by {}'.format(song, artist))
    audio_source = await FFmpegOpusAudio.from_probe(file_path, method='fallback')
    voice_client.play(audio_source)

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_disconnect():
    await voice_client.disconnect()
    print("Disconnecting!")

bot.run(token)
