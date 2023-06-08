

import discord
import os
from discord.ext import commands
from keepalive import keep_alive

token = os.environ['token_justwait']

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Erstelle einen neuen Bot-Client
bot = commands.Bot(command_prefix='?', intents=intents)

# Event: Bot erfolgreich gestartet
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="?KnockKnock"))
    print('Der Bot ist bereit!')

# Event: Nachricht empfangen
@bot.event
async def on_message(message):
    # Ignoriere Nachrichten vom Bot selbst, um Schleifen zu vermeiden
    if message.author == bot.user:
        return
    if message.content.startswith('?KnockKnock'):
        await message.channel.send('Hallo!')
    elif message.content.startswith('?join'):
        if message.author.voice is not None and message.author.voice.channel is not None:
            channel = message.author.voice.channel
            voice_client = await channel.connect()
            if voice_client.is_playing():
                voice_client.stop()
            await message.channel.send(f"Ich habe den Sprachkanal {channel.name} stumm betreten!")
        else:
            await message.channel.send("Du bist in keinem Sprachkanal!")

# Führe den Bot aus
keep_alive()
bot.run(token)