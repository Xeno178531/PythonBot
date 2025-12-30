# ------| Importy/biblioteki |------
import discord
import discord.ext
import economy as ec
import json
import leveling_system as ls
import logging
import os
import random
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# ------| Ładowanie plików początkowych |------
load_dotenv()
confFile = "config.json"
botToken = os.getenv('DISCORD_TOKEN')

# ------| Konfiguruj logowania |------
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler('discord.log', encoding='utf-8', mode='w'),
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

# ------| Cytaty |------

quotesFile = "quotes.json"

def load_config():
    with open(confFile, "r") as file:
        return json.load(file)

def save_config(data):
    with open(confFile, "w") as file:
        json.dump(data, file, indent=4)

def load_quotes():
    with open(quotesFile, "r", encoding="utf-8") as file:
        return json.load(file)
quotesls = load_quotes()

# ------| Eventy |------

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

# ------| Komendy |------

@bot.tree.command(name="hello", description="Powiedz cześć!")
async def hello_command(interaction: discord.Interaction):
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(f"Cześć {interaction.user.mention}! 👋")  #Hello

@bot.tree.command(name="ping", description="Wyświetla ping użytkownika")
async def ping_command(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # Konwersja na milisekundy
    # noinspection PyUnresolvedReferences
    await interaction.response.send_message(f'🏓 Pong! Opóźnienie: {latency}ms') #Ping

@bot.tree.command(name="pomoc", description="Wyświetla pomoc")
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

@bot.tree.command(name="poziom", description="Wyświetla twój aktualny poziom")
async def level_command(interaction:discord.Interaction):
    data = await ls.lvlMain.get_data_for(interaction.user)
    await interaction.response.send_message(f"poziom: {data.level}, znajdujesz się na {data.rank} miejscu.") #Poziom

@bot.tree.command(name="topka", description="Wyświetla listę członków z najwyższymi poziomami.")
async def lvl_top_command(interaction: discord.Interaction):
    members_data = await ls.lvlMain.each_member_data(interaction.guild, sort_by='rank', limit=10)
    if not members_data:
        await interaction.response.send_message("❌ Brak danych w rankingu!")
        return
    embed = discord.Embed(title=f"🏆 Top 10 - Ranking poziomów", description=f"Ranking członków serwera **{interaction.guild.name}**", color=discord.Color.gold(), timestamp=interaction.created_at)
    embed.set_author(name=f"Ranking • {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    ranking_text = ""

    for i, member_data in enumerate(members_data, start=1):
        place_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"][i - 1]
        ranking_text += (
            f"{place_emoji} **{member_data.name}**\n"
            f"```diff\n"
            f"+ Poziom: {member_data.level} | XP: {member_data.xp}/{ls.lvlMain.get_xp_for_level(member_data.level + 1)}\n"
            f"+ Całkowite XP: {member_data.total_xp} | Miejsce: #{member_data.rank}\n"
            f"```\n")
    embed.add_field(name="📊 Ranking", value=ranking_text if ranking_text else "Brak danych", inline=False)

    total_members = len(members_data)
    avg_level = sum(md.level for md in members_data) / total_members if total_members > 0 else 0

    embed.add_field(
        name="📈 Statystyki",
        value=(
            f"```yaml\n"
            f"Członkowie w rankingu: {total_members}\n"
            f"Średni poziom: {avg_level:.1f}\n"
            f"Najwyższy poziom: {members_data[0].level if members_data else 0}\n"
            f"```"
        ),
        inline=True
    )
    user_data = await ls.lvlMain.get_data_for(interaction.user)
    if user_data:
        embed.add_field(
            name="👤 Twoja pozycja",
            value=(
                f"```diff\n"
                f"+ Miejsce: #{user_data.rank}\n"
                f"```"
            ),
            inline=True
        )
    embed.set_footer(
        text=f"Ranking aktualny na • {interaction.guild.name}",
        icon_url=bot.user.avatar
    )

    embed.set_thumbnail(url=str(interaction.guild.icon) if interaction.guild.icon else interaction.user.display_icon)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ankieta", description="Tworzy nową ankietę")
async def poll_command(interaction: discord.Interaction, title: str, question: str):
    embed = discord.Embed(title=title, description=question)
    embed.set_footer(text=f"Ankiete utworzył {interaction.user}")
    await interaction.response.send_message(embed=embed)
    poll_msg = await interaction.original_response()
    await poll_msg.add_reaction("👍")
    await poll_msg.add_reaction("👎")

@bot.tree.command(name="cytat-nowy", description="Stwórz nowy cytat")
async def quote_command(interaction: discord.Interaction, quote: str):
    embed = discord.Embed(title="Cytat", description=quote, color=0x3d35db)
    await interaction.response.send_message(embed=embed)
    quote_msg = await interaction.original_response()
    await quote_msg.add_reaction("❤️")
    await quote_msg.add_reaction("💀")
    await quote_msg.add_reaction("🤮")

@bot.tree.command(name="cytat-random", description="Wyświetla losowy cytat")
async def quotes_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Cytat", description=random.choice(quotesls), color=0x3d35db)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info-bot", description="Pokazuje informacje o bocie")
async def botinfo_command(interaction: discord.Interaction):
    mem = psutil.virtual_memory()
    percent_ram = mem.percent
    percent_cpu = psutil.cpu_percent(interval=True)
    server_ping = round(bot.latency * 1000)
    embed = discord.Embed(title="📚 Info", description=f"🏓 Ping: **{server_ping}ms**\n🧠 Użycie RAM: **{percent_ram}%**\n⚙️ Użycie CPU: **{percent_cpu}%**", color=0xf50000)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="info-serwer", description="Pokazuje informacje o serwerze")
async def serverinfo_command(interaction: discord.Interaction):
    guild = interaction.guild
    humans = sum(1 for m in guild.members if not m.bot)
    bots = sum(1 for m in guild.members if m.bot)
    count = guild.member_count
    embed = discord.Embed(title="Serwer Info", description=f"Łączna liczba członków: {count}\nLiczba ludzi: {humans}\nLiczba botów: {bots}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="channel", description="Ustaw kanał powitań/pożegnań")
@app_commands.checks.has_permissions(administrator=True)
async def setnotifications_command(interaction: discord.Interaction, channel: discord.TextChannel):
    config = load_config()
    config["notifications_channel_id"] = channel.id
    save_config(config)
    await interaction.response.send_message(f"✅ Kanał powitań/pożegnań ustawiony na {channel.mention}", ephemeral=True)

@bot.tree.command(name="test", description="Komenda do testów.")
async def test_command(interaction: discord.Interaction):
    url = bot.user.avatar
    await interaction.response.send_message(url)

# ------| Ekonomia |------
@bot.tree.command(name="work", description="Zarabiasz gotówkę serwerową")
async def work_command(interaction: discord.Interaction):
    user_id = interaction.user.id
    cooldown = 60

    remaining = ec.check_cooldown(user_id, "work", cooldown)
    if remaining > 0:
        await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**", ephemeral=True)
        return
    
    amount = random.randint(20,100)
    ec.add_money(user_id, amount)
    ec.set_cooldown(user_id, "work")
    await interaction.response.send_message(f"{interaction.user.mention} zarobił {amount}💰!")

@bot.tree.command(name="crime", description="Odbierz dzienną nagrodę")
async def crime(interaction: discord.Interaction):
    user_id = interaction.user.id
    cooldown = 120

    remaining = ec.check_cooldown(user_id, "crime", cooldown)
    if remaining > 0:
        await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**", ephemeral=True)
        return
    
    choice = random.randint(0,1)
    if choice == 1:
        amount = random.randint(200,500)
        ec.add_money(interaction.user.id, amount)
        ec.set_cooldown(user_id, "crime")
        await interaction.response.send_message(f"Udało się! {interaction.user.mention} ukradł/a {amount}.")
    else:
        amount = random.randint(200,400)
        ec.remove_money(interaction.user.id, amount)
        ec.set_cooldown(user_id, "crime")
        await interaction.response.send_message(f"Nie udało się! {interaction.user.mention} stracił/a {amount}!")

@bot.tree.command(name="balance", description="Sprawdza stan konta")
async def balance(interaction: discord.Interaction):
    member_balance = ec.get_balance(interaction.user.id)
    await interaction.response.send_message(f"{interaction.user.mention} ma na koncie {member_balance}")

@bot.tree.command(name="daily", description="Odbierz dzienną nagrodę")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    cooldown = 86400

    remaining = ec.check_cooldown(user_id, "daily", cooldown)
    if remaining > 0:
        await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**", ephemeral=True)
        return
    
    amount = 500
    ec.add_money(user_id, amount)
    ec.set_cooldown(user_id, "daily")
    await interaction.response.send_message(f"{interaction.user.mention} odebrał codzienną nagrodę!")

@bot.tree.command(name="leaderboard", description="Pokazuje 10 najbogatszych graczy na serwerze")
async def leaderboard(interaction: discord.Interaction):
    data = ec.get_leaderboard()
    if not data:
        await interaction.response.send_message("Brak danych", ephemeral=True)
        return

    embed = discord.Embed(title="TOP 10 Najbogatszych", color=discord.Color.gold())
    for i, (user_id, member_balance) in enumerate(data, start=1):
        user = bot.get_user(user_id)
        name = user.name if user else f"ID {user_id}"
        embed.add_field(name=f"{i}. {name}", value=f"💰 {member_balance}", inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="shop", description="Pokazuje sklep")
async def shop(interaction: discord.Interaction):
    items = ec.return_items()
    text = ""
    for item, price in items.items():
        text += f"**{item}** — {price}💰\n"

    await interaction.response.send_message(embed=discord.Embed(title="🛒 Sklep", description=text))

@bot.tree.command(name="buyitem", description="Kupuje przedmiot ze sklepu")
@app_commands.describe(item="Wybierz przedmiot")
@app_commands.choices(item=ec.get_item_choices())
async def buyitem(interaction: discord.Interaction, item: app_commands.Choice[str]):
    items = ec.return_items()
    item = item.value

    if item not in items:
        print(item)
        await interaction.response.send_message("❌ Nie ma takiego itemu", ephemeral=True)
        return

    price = items[item]
    member_balance = ec.get_balance(interaction.user.id)

    if member_balance < price:
        await interaction.response.send_message("❌ Nie masz wystarczająco pieniędzy", ephemeral=True)
        return

    ec.remove_money(interaction.user.id, price)
    await interaction.response.send_message(f"✅ Kupiłeś **{item}** za {price}💰")

if botToken:
    bot.run(token=botToken)
else:
    print("❌ Błąd: Nie znaleziono tokenu DISCORD_TOKEN")
    print("Dodaj token do pliku .env lub zmiennych środowiskowych")