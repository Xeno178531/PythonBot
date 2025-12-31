# ------| Importy/biblioteki |------
import discord
import discord.ext
import economy as ec
import json
import lvl_sys as ls
import logging
import os
import random
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ------| Ładowanie plików początkowych |------

load_dotenv()
confFile = "Configs/config.json"
botToken = os.getenv('DISCORD_TOKEN')

# ------| Konfiguruj logowania |------

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler('Data/discord.log', encoding='utf-8', mode='w'),
        logging.StreamHandler()
    ]
)

# ------| Intents |------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# ------| Inicjalizacja bota |------

bot = commands.Bot(command_prefix='.', intents=intents)
print("Poprawnie zainicjowano moduł bota.")

async def discord_load_cogs():
    cogs_list = [
        'Cogs.primary',
        'Cogs.economy',
        'Cogs.lvl_sys'
    ]

    for cog in cogs_list:
        try:
            await bot.load_extension(cog)
            print(f"✅ Poprawnie załadowano moduł: {cog}.")
        except commands.ExtensionNotFound:
            print(f"⚠️ Nie znaleziono modułu: {cog}")
        except Exception as e:
            print(f"❌ Błąd ładowania {cog}: {e}")

# ------| Cytaty |------

quotesFile = "Data/quotes.json"

def load_config():
    with open(confFile, "r") as file:
        return json.load(file)

def save_config(data):
    with open(confFile, "w") as file:
        json.dump(data, file, indent=4)

def load_quotes():
    with open(quotesFile, "r", encoding="utf-8") as file:
        return json.load(file)
quotesList = load_quotes()

# ------| Eventy |------

@bot.event
async def on_ready():
    await discord_load_cogs()

    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Zsynchronizowano {len(synced)} komend")
    except Exception as e:
        print(f"⚠️  Błąd synchronizacji: {e}")
    print(f'✅ Zalogowano jako: {bot.user.name}')
    print(f'🆔 ID bota: {bot.user.id}')
    print(f'🌐 Serwery: {len(bot.guilds)}')
    print('------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await ls.lvlMain.award_xp(amount=[15, 25], message=message, refresh_name=True)  #Add EXP

@bot.event
async def on_member_join(member):
    guild = member.guild
    humans = sum(1 for m in guild.members if not m.bot)
    embed = discord.Embed(title=f"Witaj towarzyszu {member.mention}", description="Powiem wprost. Jest was za dużo. Zrobię wszystko co w mojej mocy aby się was pozbyć. Zawarłem pakt z matematyczką, I ona mi w tym pomoże.", color=0x00f51d)
    if int(humans) > 4:
        embed.set_author(name=f"Na serwerze jest {humans} osób.")
    else:
        embed.set_author(name=f"Na serwerze są {humans} osoby.")
    embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHhqNTUzY20xc2JoY2M0djFqNHJoMTJrbGM3djlrNTB4aG9icGY3YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I52WlfRLfsiXCURsgp/giphy.gif")
    channel_id = load_config().get("notifications_channel_id")

    if channel_id is None:
        return

    channel = member.guild.get_channel(channel_id)
    if channel:
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    humans = sum(1 for m in guild.members if not m.bot)
    embed = discord.Embed(title=f"Żegnaj towarzyszu {member.mention}", description="Jednego mniej", color=0x00f51d)
    if int(humans) > 4: 
        embed.set_author(name=f"Na serwerze jest {humans} osób.")
    else:
        embed.set_author(name=f"Na serwerze są {humans} osoby.")
    embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHhqNTUzY20xc2JoY2M0djFqNHJoMTJrbGM3djlrNTB4aG9icGY3YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I52WlfRLfsiXCURsgp/giphy.gif")
    channel_id = load_config().get("notifications_channel_id")

    if channel_id is None:
        return

    channel = member.guild.get_channel(channel_id)
    if channel:
        await channel.send(embed=embed)

if __name__ == '__main__':
    if botToken:
        bot.run(token=botToken)
    else:
        print("❌ Błąd: Nie znaleziono tokenu DISCORD_TOKEN")
        print("Dodaj token do pliku .env lub zmiennych środowiskowych")