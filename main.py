import logging
import os
import discord
import config
import leveling_system as ls
import sqlite3 as sq
import economy as ec
import random
import json
import psutil
from datetime import datetime
from discord.ext import commands
from discord import app_commands
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

bot = commands.Bot(command_prefix='.', intents=intents,)
print("Poprawnie zainicjowano moduł bota.")

#Pilk konfiguracyjny + Cytaty
CONFIG_FILE = "config.json"
QUOTES_FILE = "quotes.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_quotes():
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
quotesls = load_quotes()

#Eventy
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
    await bot.process_commands(message)
    await ls.lvlMain.award_xp(amount=[15, 25], message=message, refresh_name=True)  #Add EXP

@bot.event
async def on_member_join(member):
    guild = member.guild
    humans = sum(1 for m in guild.members if not m.bot)
    embed = discord.Embed(title=f"Wtaj towarzyszu {member.mention}", description="Powiem wprost. Jest was za dużo. Zrobię wszystko co w mojej mocy aby się was pozbyć. Zawarłem pakt z matematyczką, I ona mi w tym pomoże.", color=0x00f51d)
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

#Komendy
@bot.tree.command(name="quotes", description="Pokazuje losowy cytat")
async def quotes(interaction: discord.Interaction):
    embed = discord.Embed(title="Cytat", description=random.choice(quotesls), color=0x3d35db)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botinfo", description="Pokazuje informacje o bocie")
async def botinfo(interaction: discord.Interaction):
    mem = psutil.virtual_memory()
    percent_ram = mem.percent
    percent_cpu = psutil.cpu_percent(interval=True)
    ping = round(bot.latency*1000)
    embed = discord.Embed(title="📚 Info", description=f"🏓 Ping: **{ping}ms**\n🧠 Użycie RAM: **{percent_ram}%**\n⚙️ Użycie CPU: **{percent_cpu}%**", color=0xf50000)
    await interaction.response.send_message(embed=embed)

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

@bot.tree.command(name="serverinfo", description="Pokazuje informacje o serwerze")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    humans = sum(1 for m in guild.members if not m.bot)
    bots = sum(1 for m in guild.members if m.bot)
    count = guild.member_count
    embed = discord.Embed(title="Serwer Info", description=f"Łączna liczba członków: {count}\nLiczba ludzi: {humans}\nLiczba botów: {bots}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="setnotifications", description="Ustaw kanał powitań/pożegnań")
@app_commands.checks.has_permissions(administrator=True)
async def setnotifications(interaction: discord.Interaction, channel: discord.TextChannel):
    config = load_config()
    config["notifications_channel_id"] = channel.id
    save_config(config)
    await interaction.response.send_message(f"✅ Kanał powitań/pożegnań ustawiony na {channel.mention}", ephemeral=True)

@bot.tree.command(name="additem", description="Dodaje przedmiot do sklepu")
@app_commands.checks.has_permissions(administrator=True)
async def additem(interaction: discord.Interaction, name: str, price:str):
    ec.add_item(name, price)
    await interaction.response.send_message(f"Przedmiot {name} został dodany do sklepu!")

#Ekonomia
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

@bot.command()
async def shop(ctx):
    with sq.connect("economy.db") as eco:
        c = eco.cursor()
        c.execute("SELECT item, price FROM shop")
        items = c.fetchall()

    text = "\n".join(f"🛒 **{i}** — {p}💰" for i, p in items)
    await ctx.send(f"🛍️ **Sklep**\n{text}")

@bot.command()
async def buy(ctx, item: str):
    with sq.connect("economy.db") as eco:
        c = eco.cursor()

        c.execute("SELECT price FROM shop WHERE item = ?", (item,))
        result = c.fetchone()

        if not result:
            await ctx.send("❌ Taki przedmiot nie istnieje")
            return

        price = result[0]
        balance = ec.get_balance(ctx.author.id)

        if balance < price:
            await ctx.send("❌ Nie masz tyle pieniędzy")
            return

        ec.remove_money(ctx.author.id, price)
        await ctx.send(f"✅ Kupiłeś **{item}** za {price}💰")

if botToken:
    bot.run(botToken, log_handler=botHandler, log_level=logging.DEBUG)
    print("Poprawnie zainicjowano token bota")
else:
    print("❌ Błąd: Nie znaleziono tokenu DISCORD_TOKEN")
    print("Dodaj token do pliku .env lub zmiennych środowiskowych")