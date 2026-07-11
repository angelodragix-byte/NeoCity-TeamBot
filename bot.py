import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


TOKEN = 

SCHICHT_CHANNEL_ID = 1454908791647768798
TEAM_CHANNEL_ID = 1454908791647768798

SCHICHT_ROLE_ID = 1454908384917717280


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


scheduler = AsyncIOScheduler()
TEAM_MESSAGE_ID = None
team_message = None
update_started = False


ROLES = [
    ("Owner", 1454914822301810798),
    ("Co.Owner", 1454914876169392158),

    ("[PL] ✗ Projektleitung", 1454908328449802401),
    ("[Stv.PL] ✗ Stv. Projektleitung", 1454908330005762149),

    ("[DT] ✗ Direktor", 1454908333914984702),
    ("[Stv.DT] ✗ Stv. Direktor", 1459179066606223548),

    ("[MA] ✗ Manager", 1454908349585031219),
    ("[Stv.MA] ✗ Stv. Manager", 1454908354966065153),

    ("[TL] ✗ Teamleitung", 1454908342815297557),
    ("[Stv.TL] ✗ Stv. Teamleitung", 1454908344023122104),

    ("[FV] ✗ Fraktionsverwaltung", 1454908358397133063),
    ("[Stv.FV] ✗ Stv. Fraktionsverwaltung", 1454908359978389648),

    ("[AS] ✗ Ausbilder", 1462098796094685226),
    ("[Stv.AS] ✗ Stv. Ausbilder", 1462099113058504738),

    ("[EL] ✗ Eventleitung", 1454908363715645605),
    ("[Stv.EL] ✗ Stv. Eventleitung", 1454908361966489611),

    ("[Head Admin] ✗ Head Administrator", 1454908366546534450),
    ("[Sr.Admin] ✗ Sr. Administrator", 1454908367880323072),
    ("[Admin] ✗ Administrator", 1454908368815788079),
    ("[Jr.Admin] ✗ Jr. Administrator", 1454908370179067957),
    ("[Head Mod] ✗ Head Moderator", 1454908372158775504),
    ("[Sr.Mod] ✗ Sr. Moderator", 1454908373324533905),
    ("[Mod] ✗ Moderator", 1454908375082205327),
    ("[Jr.Mod] ✗ Jr. Moderator", 1454908377028100128),

    ("[Head Sup] ✗ Head Supporter", 1454933539320500336),
    ("[Sr.Sup] ✗ Sr. Supporter", 1454933353248587887),
    ("[Sup] ✗ Supporter", 1454908379633025268),
    ("[T-Sup] ✗ Test Supporter", 1454908381348499693)
]
def create_embed(guild):

    text = ""
    online = 0
    offline = 0
    total = 0

    for role_name, role_id in ROLES:

        role = guild.get_role(role_id)

        if role is None:
            continue

        members = role.members

        text += f"**{role.mention}**\n"

        if members:

            for member in members:

                if member.status == discord.Status.offline:
                    status = "🔴"
                    offline += 1
                else:
                    status = "🟢"
                    online += 1

                text += f"{status} {member.mention} | {member.name}\n"

                total += 1

        else:
            text += "(Kein Mitglied)\n"

        text += "\n"


    embed = discord.Embed(
        title=f"🌀 NeoCity Teamliste                      👥Team Mitglieder[{total}]",
        color=0xff69b4
    )

    embed.description = text

    embed.set_footer(
    text=(
        f"Aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M')} | "
        f"🟢 Online: {online} | "
        f"🔴 Offline: {offline} | "
        f"🔵 Gesamt: {total}"
    )

    
        
          
    

        
            
            
       
    )

    return embed



@tasks.loop(minutes=5)
async def auto_update():

    global team_message

    if team_message:

        await team_message.edit(
            embed=create_embed(team_message.guild)
        )



nachricht = """
**📅 Schichtplan**

<@&1525222193976443053>

Bitte tragt euch täglich in eine Schicht ein.

🔴 **12:00 – 18:00**
🟠 **16:00 – 00:00**
🟡 **10:00 – 20:00**
🟢 **08:00 – 22:00**

Reagiert mit der passenden Emoji-Farbe.
"""


async def sende_schicht():

    kanal = bot.get_channel(SCHICHT_CHANNEL_ID)

    if kanal:

        msg = await kanal.send(nachricht)

        for emoji in [
            "🔴",
            "🟠",
            "🟡",
            "🟢"
        ]:
            await msg.add_reaction(emoji)

        print("Schichtplan gesendet")



@bot.event
async def on_ready():

    global update_started

    print(f"{bot.user} ist online!")

    if not update_started:

        auto_update.start()

        scheduler.add_job(
            sende_schicht,
            "cron",
            hour=10,
            minute=13
        )

        scheduler.start()

        update_started = True

        print("Alle Systeme laufen!")



@bot.command()
async def team(ctx):

    global team_message

    embed = create_embed(ctx.guild)

    if team_message is None:

        team_message = await ctx.send(
            embed=embed
        )

    else:

        await team_message.edit(
            embed=embed
        )



@bot.command()
async def schicht(ctx):

    await sende_schicht()

    await ctx.send(
        "✅ Schichtplan gesendet!"
    )



@bot.command()
async def ping(ctx):

    await ctx.send(
        "🏓 Pong!"
    )

import os

bot.run(os.getenv("MTUyMTUzNzU1MzQ1NzYxMDc1Mg.GFlopy.Vz0Gga9yy2tzmnD2AHS316fVkOtDZ8rk0Y4kIQ")


