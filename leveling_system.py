import discord
import os
from datetime import datetime
from discordLevelingSystem import DiscordLevelingSystem, LevelUpAnnouncement, RoleAward


# Leveling
lvlDefaultMentions = discord.AllowedMentions()
lvlDbFile = os.path.join('Data', 'DiscordLevelingSystem.db')
lvlMainGuild = 1452724850149036145
lvlAwards = {
    lvlMainGuild: [
        RoleAward(role_id=831672678586777601, level_requirement=1, role_name='Nowy'),
        RoleAward(role_id=831672678586777602, level_requirement=2, role_name='Bywalec'),
        RoleAward(role_id=831672678586777603, level_requirement=3, role_name='Mieszkaniec'),
        RoleAward(role_id=831672678586777604, level_requirement=4, role_name='Masz swój dom ?'),
        RoleAward(role_id=831672678586777605, level_requirement=5, role_name='On nie ma domu...'),
    ]
}
lvlMessage = discord.Embed(
    title=f"{LevelUpAnnouncement.Member.name} wskoczył na wyższy poziom ! 🎉",
    description=f"Gratulacje {LevelUpAnnouncement.Member.mention}, właśnie osiągnąłeś **{LevelUpAnnouncement.LEVEL}** poziom. Tak trzymaj !",
    colour=0xe5a50a,
    timestamp=datetime.now())
lvlMessage.set_image(
    url=LevelUpAnnouncement.Member.banner_url)
lvlMessage.set_thumbnail(
    url=LevelUpAnnouncement.Member.avatar_url)
lvlMessage.set_footer(
    text="Niech Kliś ci błogosławi",
    icon_url=LevelUpAnnouncement.Member.avatar_url)

lvlAnnouncement = LevelUpAnnouncement(lvlMessage)

lvlChannel = 1453793052823916616
lvlMain = DiscordLevelingSystem(rate=1,
                                per=60.0,
                                awards=lvlAwards,
                                level_up_announcement=lvlAnnouncement)
# lvlUpMessage = LevelUpAnnouncement(message=lvlMessage,
#                                    level_up_channel_ids=[lvlChannel],
#                                    allowed_mentions=lvlDefaultMentions,
#                                    tts=False,
#                                    delete_after=None,
#                                    )

if not os.path.exists('Data'):
    os.makedirs('Data')
    print(f"Utworzono katalog: {'Data'}")
else:
    print(f"Katalog baz danych: {'Data'} istnieję - pomijam")
    
if not os.path.exists(lvlDbFile):
    print("Tworzę nową bazę danych...")
    lvlMain.create_database_file('Data')
    print(f"Utworzono: {lvlDbFile}")
else:
    print(f"Katalog baz danych: {'Data'} istnieję - pomijam")

print("🔧 Tworzę instancję systemu poziomów...")
print(f"🔗 Łączę się z bazą: {lvlDbFile}")
lvlMain.connect_to_database_file(lvlDbFile)
print("System poziomów gotowy do użycia!")
