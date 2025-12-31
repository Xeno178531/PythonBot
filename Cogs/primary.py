import discord
from discord.ext import commands
from discord import app_commands


class Primary(commands.Cog):
    """Podstawowe komendy borta"""

    def __init__(self, bot):
        self.bot = bot

    # =========== EVENTY w Cogach ===========
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Moduł 'Primary' został załadowany!")


    # =========== SLASH COMMANDS ===========


    @app_commands.command(name="hello", description="Powiedz cześć!")
    async def hello_command(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f"Cześć {interaction.user.mention}! 👋")  # Hello

    @app_commands.command(name="ping", description="Wyświetla ping użytkownika")
    async def ping_command(self, interaction: discord.Interaction):
        latency = round(bot.latency * 1000)  # Konwersja na milisekundy
        
        await interaction.response.send_message(f'🏓 Pong! Opóźnienie: {latency}ms')  # Ping

    @app_commands.command(name="pomoc", description="Wyświetla pomoc")
    async def help_command(self, interaction: discord.Interaction):
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

        await interaction.response.send_message(embed=embed)  # Pomoc

    @app_commands.command(name="ankieta", description="Tworzy nową ankietę")
    async def poll_command(self, interaction: discord.Interaction, title: str, question: str):
        embed = discord.Embed(title=title, description=question)
        embed.set_footer(text=f"Ankiete utworzył {interaction.user}")
        await interaction.response.send_message(embed=embed)
        poll_msg = await interaction.original_response()
        await poll_msg.add_reaction("👍")
        await poll_msg.add_reaction("👎")

    @app_commands.command(name="cytat-nowy", description="Stwórz nowy cytat")
    async def quote_command(self, interaction: discord.Interaction, quote: str):
        embed = discord.Embed(title="Cytat", description=quote, color=0x3d35db)
        await interaction.response.send_message(embed=embed)
        quote_msg = await interaction.original_response()
        await quote_msg.add_reaction("❤️")
        await quote_msg.add_reaction("💀")
        await quote_msg.add_reaction("🤮")

    @app_commands.command(name="cytat-random", description="Wyświetla losowy cytat")
    async def quotes_command(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Cytat", description=random.choice(quotesls), color=0x3d35db)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info-bot", description="Pokazuje informacje o bocie")
    async def botinfo_command(self, interaction: discord.Interaction):
        mem = psutil.virtual_memory()
        percent_ram = mem.percent
        percent_cpu = psutil.cpu_percent(interval=True)
        server_ping = round(bot.latency * 1000)
        embed = discord.Embed(title="📚 Info",
                              description=f"🏓 Ping: **{server_ping}ms**\n🧠 Użycie RAM: **{percent_ram}%**\n⚙️ Użycie CPU: **{percent_cpu}%**",
                              color=0xf50000)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info-serwer", description="Pokazuje informacje o serwerze")
    async def serverinfo_command(self, interaction: discord.Interaction):
        guild = interaction.guild
        humans = sum(1 for m in guild.members if not m.bot)
        bots = sum(1 for m in guild.members if m.bot)
        count = guild.member_count
        embed = discord.Embed(title="Serwer Info",
                              description=f"Łączna liczba członków: {count}\nLiczba ludzi: {humans}\nLiczba botów: {bots}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="channel", description="Ustaw kanał powitań/pożegnań")
    @app_commands.checks.has_permissions(administrator=True)
    async def setnotifications_command(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = load_config()
        config["notifications_channel_id"] = channel.id
        save_config(config)
        await interaction.response.send_message(f"✅ Kanał powitań/pożegnań ustawiony na {channel.mention}",
                                                ephemeral=True)

    @app_commands.command(name="test", description="Komenda do testów.")
    async def test_command(self, interaction: discord.Interaction):
        url = bot.user.avatar
        await interaction.response.send_message(url)


async def setup(bot):
    await bot.add_cog(Primary(bot))