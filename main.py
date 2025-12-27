import logging
import os
import discord
import config
import leveling_system as ls
import sqlite3
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from discordLevelingSystem import LevelUpAnnouncement



load_dotenv()
botToken = os.getenv('DISCORD_TOKEN')
botHandler = logging.FileHandler(filename='discord.log',
                                 encoding='utf-8',
                                 mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='?', intents=intents,)
print("Poprawnie zainicjowano moduł bota.")

if not os.path.exists(config.DATABASE_DIR):
    os.makedirs(config.DATABASE_DIR)
    print(f"Utworzono katalog: {config.DATABASE_DIR}")
else:
    print(f"Katalog baz danych: {config.DATABASE_DIR} istnieję - pomijam")

@bot.event
async def on_ready():
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Zsynchronizowano {len(synced)} komend")
    except Exception as e:
        print(f"⚠️  Błąd synchronizacji: {e}")
    print(f'✅ Zalogowano jako: {bot.user.name}')
    print(f'🆔 ID bota: {bot.user.id}')
    print(f'🌐 Serwery: {len(bot.guilds)}')
    print('------') #On Ready

@bot.event
async def on_message(message):
    await ls.lvlMain.award_xp(amount=[15, 25], message=message, refresh_name=True)  #Add EXP

@bot.tree.command(
    name="hello",
    description="Powiedz cześć!")
async def hello_command(interaction: discord.Interaction):
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(f"Cześć {interaction.user.mention}! 👋")  #Hello

@bot.tree.command(
    name="ping",
    description="Wyświetla ping użytkownika")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # Konwersja na milisekundy
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(f'🏓 Pong! Opóźnienie: {latency}ms') #Ping

@bot.tree.command(
    name="pomoc",
    description="Wyświetla pomoc")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Pomoc",
                          description="**Znajdziesz tu informacje o bocie i jego komendach**\n** **",
                          colour=0x1c71d8,
                          timestamp=datetime.now())

    embed.set_author(name="Flover Bot",
                     icon_url="https://i.imgur.com/vKeFJI1.jpeg")

    embed.add_field(name="🏓・Ping",
                    value="`/ping` ―  Wyświetla aktualny ping użytkownika \n** **",
                    inline=False)
    embed.add_field(name="🆘・Pomoc",
                    value="`/pomoc` ―  Wyświetla tą wiadomość - informacje o komendach i bocie\n** **",
                    inline=False)
    embed.add_field(name="📜 ・Cytat",
                    value="`/cytat` ―  Wyświetla losowy cytat mgr. Klisia\n** **",
                    inline=False)
    embed.add_field(name="📜 ・Poziom",
                    value="`/poziom` ― wyświetla twój poziom i aktualne miejsce w rankingu \n** **",
                    inline=False)
    embed.set_image(url="https://i.imgur.com/PMgxZfz.jpeg")
    embed.set_footer(text="Jak Jan chrzcił wodą tak ja was chrzczę Wodą z Klozeta",
                     icon_url="https://i.imgur.com/vKeFJI1.jpeg")

    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(embed=embed) #Pomoc

@bot.tree.command(
    name="poziom",
    description="Wyświetla twój aktualny poziom"
)
async def level_command(interactions:discord.Interaction):
    data = await ls.lvlMain.get_data_for(interactions.user)
    # noinspection PyUnresolvedReferences
    await interactions.response.send_message(f"poziom: {data.level}, znajdujesz się na {data.rank} miejscu.") #Poziom

@bot.tree.command(
    name="topka",
    description="Wyświetla listę członków z najwyższymi poziomami."
)
async def lvl_top_command(interactions: discord.Interaction):
        data = await ls.lvlMain.each_member_data(interactions.guild, sort_by='rank')
        # noinspection PyUnresolvedReferences
        await interactions.response.send_message(data) #Topka

if botToken:
    bot.run(botToken, log_handler=botHandler, log_level=logging.DEBUG)
    print("Poprawnie zainicjowano token bota")
else:
    print("❌ Błąd: Nie znaleziono tokenu DISCORD_TOKEN")
    print("Dodaj token do pliku .env lub zmiennych środowiskowych")


