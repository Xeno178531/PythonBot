import logging
import os
import discord
import config
import leveling_system as ls
import sqlite3
import economy as ec
import random
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

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def job(ctx):
    amount = random.randint(20,100)
    ec.add_money(ctx.author.id, amount)
    await ctx.send(f"{ctx.author.mention} zarobił {amount}💰!")
@job.error
async def job_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = ec.check_cooldown(ctx.author.id, "job", 60)
        if remaining > 0:
            await ctx.send(f"⏳ Poczekaj {ec.format_time(remaining)}")
            return

@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def crime(ctx):
    choice = random.randint(0,1)
    if choice == 1:
        amount = random.randint(200,500)
        ec.add_money(ctx.author.id, amount)
    else:
        amount = random.randint(200,400)
        ec.remove_money(ctx.author.id, amount)
@crime.error
async def crime_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = ec.check_cooldown(ctx.author.id, "crime", 120)
        if remaining > 0:
            await ctx.send(f"⏳ Poczekaj {ec.format_time(remaining)}")
            return

@bot.command()
async def bal(ctx):
    balance = ec.get_balance(ctx.author.id)
    await ctx.send(f"{ctx.author.mention} ma na koncie {balance}")

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    amount = 500
    ec.add_money(ctx.author.id, amount)
    await ctx.send(f"{ctx.author.mention} odebrał codzienną nagrodę!")
@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining = ec.check_cooldown(ctx.author.id, "daily", 86400)
        if remaining > 0:
            await ctx.send(f"⏳ Poczekaj {ec.format_time(remaining)}")
            return

@bot.command()
async def top(ctx):
    data = ec.get_leaderboard()

    if not data:
        await ctx.send("Brak danych")
        return

    embed = discord.Embed(title="TOP 10 Najbogatszych", color=discord.Color.gold())

    for i, (user_id, balance) in enumerate(data, start=1):
        user = bot.get_user(user_id)
        name = user.name if user else f"ID {user_id}"
        embed.add_field(name=f"{i}. {name}", value=f"💰 {balance}", inline=False)

    await ctx.send(embed=embed)
