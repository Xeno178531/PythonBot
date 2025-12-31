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
        'Cog.primary'
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

if __name__ == '__main__':
    if botToken:
        bot.run(token=botToken)
    else:
        print("❌ Błąd: Nie znaleziono tokenu DISCORD_TOKEN")
        print("Dodaj token do pliku .env lub zmiennych środowiskowych")