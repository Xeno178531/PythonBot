import discord
import lvl_sys as ls
from discord.ext import commands
from discord import app_commands


class LvlSystem(commands.Cog):
    """Komendy poziomów"""
    def __init__(self, bot):
        self.bot = bot

    # =========== EVENTY w Cogach ===========
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Moduł 'LvlSys' został załadowany!")


    # =========== SLASH COMMANDS ===========
    @app_commands.command(name="poziom", description="Wyświetla twój aktualny poziom")
    async def level_command(self, interaction: discord.Interaction):
        data = await ls.lvlMain.get_data_for(interaction.user)
        await interaction.response.send_message(
            f"poziom: {data.level}, znajdujesz się na {data.rank} miejscu.")  # Poziom

    @app_commands.command(name="topka", description="Wyświetla listę członków z najwyższymi poziomami.")
    async def lvl_top_command(self, interaction: discord.Interaction):
        members_data = await ls.lvlMain.each_member_data(interaction.guild, sort_by='rank', limit=10)
        if not members_data:
            await interaction.response.send_message("❌ Brak danych w rankingu!")
            return
        embed = discord.Embed(title=f"🏆 Top 10 - Ranking poziomów",
                              description=f"Ranking członków serwera **{interaction.guild.name}**",
                              color=discord.Color.gold(), timestamp=interaction.created_at)
        embed.set_author(name=f"Ranking • {interaction.user.display_name}",
                         icon_url=interaction.user.display_avatar.url)
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
            icon_url=self.bot.user.avatar
        )

        embed.set_thumbnail(
            url=str(interaction.guild.icon) if interaction.guild.icon else interaction.user.display_icon)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(LvlSystem(bot))