import discord
import economy as ec
from discord.ext import commands
from discord import app_commands


class Economy(commands.Cog):
    """Komendy ekonomi"""

    def __init__(self, bot):
        self.bot = bot

    # =========== EVENTY w Cogach ===========
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Moduł 'Economy' został załadowany!")


    # =========== SLASH COMMANDS ===========
    @app_commands.command(name="work", description="Zarabiasz gotówkę serwerową")
    async def work_command(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        cooldown = 60

        remaining = ec.check_cooldown(user_id, "work", cooldown)
        if remaining > 0:
            await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**",
                                                    ephemeral=True)
            return

        amount = random.randint(20, 100)
        ec.add_money(user_id, amount)
        ec.set_cooldown(user_id, "work")
        await interaction.response.send_message(f"{interaction.user.mention} zarobił {amount}💰!")

    @app_commands.command(name="crime", description="Odbierz dzienną nagrodę")
    async def crime(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        cooldown = 120

        remaining = ec.check_cooldown(user_id, "crime", cooldown)
        if remaining > 0:
            await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**",
                                                    ephemeral=True)
            return

        choice = random.randint(0, 1)
        if choice == 1:
            amount = random.randint(200, 500)
            ec.add_money(interaction.user.id, amount)
            ec.set_cooldown(user_id, "crime")
            await interaction.response.send_message(f"Udało się! {interaction.user.mention} ukradł/a {amount}.")
        else:
            amount = random.randint(200, 400)
            ec.remove_money(interaction.user.id, amount)
            ec.set_cooldown(user_id, "crime")
            await interaction.response.send_message(f"Nie udało się! {interaction.user.mention} stracił/a {amount}!")

    @app_commands.command(name="balance", description="Sprawdza stan konta")
    async def balance(self, interaction: discord.Interaction):
        member_balance = ec.get_balance(interaction.user.id)
        await interaction.response.send_message(f"{interaction.user.mention} ma na koncie {member_balance}")

    @app_commands.command(name="daily", description="Odbierz dzienną nagrodę")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        cooldown = 86400

        remaining = ec.check_cooldown(user_id, "daily", cooldown)
        if remaining > 0:
            await interaction.response.send_message(f"⏳ Poczekaj jeszcze **{ec.format_time(remaining)}**",
                                                    ephemeral=True)
            return

        amount = 500
        ec.add_money(user_id, amount)
        ec.set_cooldown(user_id, "daily")
        await interaction.response.send_message(f"{interaction.user.mention} odebrał codzienną nagrodę!")

    @app_commands.command(name="leaderboard", description="Pokazuje 10 najbogatszych graczy na serwerze")
    async def leaderboard(self, interaction: discord.Interaction):
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

    @app_commands.command(name="shop", description="Pokazuje sklep")
    async def shop(self, interaction: discord.Interaction):
        items = ec.return_items()
        text = ""
        for item, price in items.items():
            text += f"**{item}** — {price}💰\n"

        await interaction.response.send_message(embed=discord.Embed(title="🛒 Sklep", description=text))

    @app_commands.command(name="buyitem", description="Kupuje przedmiot ze sklepu")
    @app_commands.describe(item="Wybierz przedmiot")
    @app_commands.choices(item=ec.get_item_choices())
    async def buyitem(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
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


async def setup(bot):
    await bot.add_cog(Economy(bot))