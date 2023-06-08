import discord
import os
import asyncio
from discord.ext import commands
import time
from keepalive import keep_alive

token = os.environ['token_justwait']

global daten
daten = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a new bot client
bot = commands.Bot(command_prefix='?', intents=intents)

# Daten aus der Datei lesen
def lese_daten_aus_datei(dateiname):
    try:
        with open(dateiname, 'r') as datei:
            daten = datei.read().splitlines()
            return daten
    except FileNotFoundError:
        return []

# Daten in die Datei schreiben
def schreibe_daten_in_datei(dateiname, daten):
    with open(dateiname, 'w') as datei:
        for eintrag in daten:
            datei.write(str(eintrag) + '\n')

# Kanal aus der Datei entfernen
def entferne_kanal_aus_datei(dateiname, kanal_name):
    daten = lese_daten_aus_datei(dateiname)
    daten = [eintrag for eintrag in daten if eintrag != kanal_name]
    schreibe_daten_in_datei(dateiname, daten)

async def check_role(roles):
    role_list = ['Freund', '(Admin)', 'Member', 'Delta Force', 'BOT', 'Task Force']  # Liste der erlaubten Rollen

    for role in roles:
        if role in role_list:
            return True

    return False

async def return_def(message):
  print("return")
  await asyncio.sleep(20)
  async for msg in message.channel.history(limit=None):
            if msg.id < 1115370144617730158 or msg.id > 1115651353688154183:
                time.sleep(0.5)
                await msg.delete()     
  return
        
# Variable aktualisieren und in die Datei schreiben
print(daten)

# Event: Bot successfully started
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="?KnockKnock"))
    print('Der Bot ist bereit!')

# Event: Message received
@bot.event
async def on_message(message):
    dateiname = 'notknock.txt'
    daten = lese_daten_aus_datei(dateiname)
    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
    channel_id = message.channel.id
    author = message.author.name
    channel = bot.get_channel(1116039835828883507)  # knockknock logs
    channel_list = ["Zzz", "das-büro", "╔┃Rekruten", "╠┃Lobby 1", "╠┃Lobby 2", "╠┃Lobby 3", "╠┃Lobby 4", "╠┃Mission 1", "╠┃Mission 2", "╠┃Ausbildung 1", "╠┃Ausbildung 2", "╠┃Ausbildung 3", "╠┃Pausenraum", "╠┃Event Vorbereitung", "╠┃Team 1", "╠┃Team 2", "╠┃Büro Maurica", "╚┃Parlament Büro", "╠┃Generäle", "╠┃Büro ByD", "╠┃Büro Iceman/Blackstar", "╚┃Büro Reiner", "╠┃Verwaltungs-Talk", "╠┃Büro Albert", "╚┃Büro Frank Reich", "╚┃Feldjäger-Talk", "╚┃Infanterie", "╚┃Fallschirmjäger Talk", "╠┃Luftwaffe", "╚┃Leitung", "╚┃Gebirgsjäger", "╠┃Delta-Talk", "╚┃Auszubildende", "╚┃Einzelkämpfer Talk", "╚┃Panzergrenadiere", "╚┃Talk", "Büro Developer",]
  
    if message.channel.id == 1115370144617730158:
        # Ignore messages from the bot itself to avoid loops
        if message.author == bot.user:
            await return_def(message)
        if message.content.startswith('?KnockKnock'):
            channel_name = message.content[12:]  # Extract the voice channel name from the message content
            if channel_name not in channel_list:
                  for i in channel_list:
                      index = channel_list.index(i)
                      if int(channel_name) == index:
                          channel_name = i
                          break
                  
                  if channel_name not in daten:
                    voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                  else:
                    await message.channel.send("Du kannst in diesem Kanal nicht anklopfen!")
                    await return_def(message)
            else:
                if channel_name not in daten:
                  voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                else:
                  await message.channel.send("Du kannst in diesem Kanal nicht anklopfen!")
                  await return_def(message)
            
            if voice_channel:
                try:
                    voice_client = await voice_channel.connect()
                    member = voice_client.guild.get_member(bot.user.id)
                    if member:
                        await message.channel.send("Knock Knock joined voice channel")
                        await member.edit(nick="Knock Knock")
                        await asyncio.sleep(2)
                        await member.edit(nick="from...")
                        await asyncio.sleep(2)
                        await member.edit(nick=message.author.name)
                        await asyncio.sleep(2)
                        await member.edit(nick="[Task-09] Knock Knock")
                    await voice_client.disconnect()
                    # Send a message with information about the voice channel and author
                    
                    await channel.send(f"KnockKnock\nTimestamp: {timestamp}\nVoice Channel: {voice_channel}\nAuthor: {author}\n?KnockKnock\n\n")
                    print("***")
                    print(f"Voice channel left\nTimestamp: {timestamp}\nVoice Channel: {voice_channel}\nAuthor: {author}")
                    print("***")
                except discord.ClientException:
                    await message.channel.send("Ich kann dem Sprachkanal nicht beitreten.")
            else:
                await message.channel.send("Der angegebene Sprachkanal existiert nicht.")

        if message.content.startswith('?channels'):
          cont = ""
          for i in channel_list:
            index = channel_list.index(i)
            cont += f"{index} : {i}\n"
          await message.channel.send(str(cont))
          
          await channel.send(f"KnockKnock\nTimestamp: {timestamp}\nAuthor: {author}\n?channels\n\n")
          await asyncio.sleep(5)

        if message.content.startswith('?delete'):
          async for msg in message.channel.history(limit=None):
                if msg.id < 1115370144617730158 or msg.id > 1115651353688154183:
                    time.sleep(0.5)
                    await msg.delete()

        if message.content.startswith('?notKnock'):
            channel_name = message.content[10:]  # Extract the voice channel name from the message conten
            author_roles = [role.name for role in message.author.roles]
            has_allowed_role = await check_role(author_roles)
            if has_allowed_role == True:
                if channel_name not in channel_list:
                      for i in channel_list:
                          index = channel_list.index(i)
                          if int(channel_name) == index:
                              channel_name = i
                              break
                      
                      if channel_name not in daten:
                        voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                      else:
                        await message.channel.send("Du hast diesen Channel bereits ausgeschlossen")
                        await message.channel.send(f"Ausgeschlossene Channels: {daten}")
                        await return_def(message)
                else:
                    if channel_name not in daten:
                        voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                    else:
                        await message.channel.send("Du hast diesen Channel bereits ausgeschlossen")
                        await message.channel.send(f"Ausgeschlossene Channels: {daten}")
                        await return_def(message)

                # Variable aktualisieren und in die Datei schreiben
                dateiname = 'notknock.txt'
                daten = lese_daten_aus_datei(dateiname)
                daten.append(str(voice_channel.name))  # Speichern Sie den Namen des Sprachkanals anstelle des VoiceChannel-Objekts
                schreibe_daten_in_datei(dateiname, daten)
                await message.channel.send(f"{daten[len(daten) - 1]} wurde ausgeschlossen!")
                await channel.send(f"KnockKnock\nTimestamp: {timestamp}\nVoice Channel: {voice_channel}\nAuthor: {author}\n?notKnock\n\n")

            else:
              await message.channel.send("Du hast nicht die ausreichenden Berechtigungen für diese Aktion!")
              await message.channel.send("Ist das ein Fahler? Wende die an @[Technik] Just Wait ...")
              await return_def(message)

        if message.content.startswith('?reKnock'):
          channel_name = message.content[9:]  # Extract the voice channel name from the message content
          author_roles = [role.name for role in message.author.roles]
          has_allowed_role = await check_role(author_roles)
          if has_allowed_role == True:
            if channel_name not in channel_list:
                      for i in channel_list:
                          index = channel_list.index(i)
                          if int(channel_name) == index:
                              channel_name = i
                              break
                      
                      if channel_name in daten:
                        voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                      else:
                        await message.channel.send("Dieser Kanal ist bereits freigegeben!")
                        if daten != []:
                           await message.channel.send(f"Ausgeschlossene Channels: {daten}")
                        else:
                          await message.channel.send("Keine Channels sind deaktiviert!")
                          await return_def(message)
            else:
                  if channel_name in daten:
                        voice_channel = discord.utils.get(message.guild.voice_channels, name=channel_name)
                  else:
                        await message.channel.send("Dieser Kanal ist bereits freigegeben!")
                        if daten != []:
                           await message.channel.send(f"Ausgeschlossene Channels: {daten}")
                        else:
                          await message.channel.send("Keine Channels sind deaktiviert!")
                          await return_def(message)
              
            # Beispielaufruf der Funktion
            dateiname = 'notknock.txt'
            entferne_kanal_aus_datei(dateiname, channel_name)
            print(daten)
            await message.channel.send(f"Der Channel {daten} ist wieder freigegeben")
            
            await channel.send(f"KnockKnock\nTimestamp: {timestamp}\nAuthor: {author}\n?reKnock\n\n")

          else:
              await message.channel.send("Du hast nicht die ausreichenden Berechtigungen für diese Aktion!")
              await message.channel.send("Ist das ein Fahler? Wende die an @[Technik] Just Wait ...")
              await return_def(message)
                  
    await bot.process_commands(message)
          
# Run the bot
keep_alive()
bot.run(token)
