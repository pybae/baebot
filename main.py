from discord.ext import commands
import discord
from discord import opus
from discord import FFmpegOpusAudio
from music import search_songs, find_lyrics
import ctypes
import os

token = os.getenv('BAEBOT_TOKEN')
if token:
    print("Initializing baebot with token: " + token)
else:
    print("No BAEBOT_TOKEN found. Set BAEBOT_TOKEN and retry")
    sys.exit()

bot = commands.Bot(command_prefix='$')

discord.opus.load_opus("libopus.so.0")
print(discord.opus.is_loaded())

def get_voice_client():
    return bot.voice_clients[0] if len(bot.voice_clients) > 0 else None

@bot.command(help="Searches for and plays a song by title or artist")
async def play(ctx, arg):
    voice_client = get_voice_client()
    if not voice_client:
        voice_channel = bot.get_channel(570805084087255071)
        voice_client = await voice_channel.connect()
    elif voice_client.is_playing():
        voice_client.pause()

    (song, artist, file_path) = search_songs(arg)
    await ctx.send('Now playing {} by {}'.format(song, artist))
    audio_source = await FFmpegOpusAudio.from_probe(file_path, method='fallback')
    voice_client.play(audio_source)

@bot.command(help="Pauses the current track")
async def pause(ctx):
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send('Pausing')
    else:
        await ctx.send('No track is playing')

@bot.command(help="Resumes the current track")
async def resume(ctx):
    voice_client = get_voice_client()
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send('Resuming')
    else:
        await ctx.send('No track is paused')

@bot.command(help="Searches for lyrics with the specified title and artist")
async def lyrics(ctx, title, artist=""):
    lyrics = find_lyrics(title, artist)

    break_index = lyrics.find('\n\n', 1000)
    while break_index != -1 and len(lyrics) > 1500:
        chunk = "```" + lyrics[:break_index] + "```"
        lyrics = lyrics[break_index + 2:]
        break_index = lyrics.find('\n\n')
        await ctx.send(chunk)
    await ctx.send("```" + lyrics + "```")

@bot.command(help="Deletes the most recent n messages")
async def clean(ctx, n):
    n = int(n)
    i, to_be_deleted = 0, []
    for message in bot.cached_messages:
        if bot.user == message.author:
            to_be_deleted.append(message)
    for message in to_be_deleted[::-1][:n]:
        await message.delete()
    await ctx.send("Deleted last " + str(n) + " messages")

@bot.event
async def on_ready():
    print("Ready!")

@bot.event
async def on_disconnect():
    await voice_client.disconnect()
    print("Disconnecting!")

bot.run(token)
