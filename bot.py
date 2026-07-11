import os
from datetime import datetime

from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

from apscheduler.schedulers.asyncio import AsyncIOScheduler


# ==========================
# TOKEN LADEN
# ==========================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ Kein Discord Token gefunden!")
    print("Erstelle eine .env Datei:")
    print("TOKEN=DEIN_TOKEN")
    exit()


# ==========================
# DISCORD SETUP
# ==========================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.presences = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


scheduler = AsyncIOScheduler()


# ==========================
# TEAM ROLLEN
# ==========================

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


team_message = None


# ==========================
# TEAM EMBED
# ==========================

def create_team_embed(guild):

    text = ""

    online = 0
    offline = 0
    total = 0


    for role_name, role_id in ROLES:

        role = guild.get_role(role_id)

        if role is None:
            continue


        members = role.members


        text += f"**{role.mention} • {len(members)} Mitglieder**\n"


        for member in members:

            if member.status == discord.Status.offline:
                status = "🔴"
                offline += 1

            else:
                status = "🟢"
                online += 1


            text += f"{status} {member.mention} | {member.name}\n"

            total += 1


        if not members:
            text += "(Kein Mitglied)\n"


        text += "\n"


    embed = discord.Embed(
        title=f"🌀 NeoCity Teamliste                 👥Team Mitglieder[{total}]",
        description=text or "Keine Mitglieder",
        color=0xff69b4
    )


    embed.set_footer(
        text=(
            f"Update: {datetime.now().strftime('%d.%m.%Y %H:%M')} | "
            f"🟢 Online {online}  |  🔴 Offline {offline}"
        )
    )


    return embed
# ==========================
# SCHICHTPLAN
# ==========================

SCHICHT_CHANNEL = 1454908791647768798


schicht_text = """
**📅 NeoCity Schichtplan**

——Staff Team—— <@&1525222193976443053

Bitte tragt euch täglich in eine Schicht ein.

Wenn ihr euch nicht eintragt und nicht abmeldet,
werden Teamwarns verteilt!


🔴 **13:00 - 16:00**

🟠 **16:00 - 19:00**

🟡 **19:00 - 22:00**

🟢 **22:00 - 00:00**


Reagiert mit der passenden Emoji-Farbe.
"""


async def sende_schicht():

    kanal = bot.get_channel(
        SCHICHT_CHANNEL
    )


    if kanal is None:
        print("❌ Schicht-Kanal nicht gefunden")
        return


    msg = await kanal.send(
        schicht_text
    )


    for emoji in [
        "🔴",
        "🟠",
        "🟡",
        "🟢"
    ]:

        await msg.add_reaction(
            emoji
        )


    print("✅ Schichtplan gesendet")



# ==========================
# TEAM AUTO UPDATE
# ==========================

@tasks.loop(minutes=5)
async def update_team():

    global team_message


    if team_message:

        await team_message.edit(
            embed=create_team_embed(
                team_message.guild
            )
        )



# ==========================
# BOT START
# ==========================

@bot.event
async def on_ready():

    print("==============================")
    print(f"✅ Bot online: {bot.user}")
    print(f"✅ Server: {len(bot.guilds)}")
    print("==============================")


    if not update_team.is_running():
        update_team.start()


    if not scheduler.running:

        scheduler.add_job(
            sende_schicht,
            "cron",
            hour=10,
            minute=0
        )


        scheduler.start()
# ==========================
# COMMANDS
# ==========================


@bot.command()
async def team(ctx):

    global team_message


    embed = create_team_embed(
        ctx.guild
    )


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
        "✅ Schichtplan wurde gesendet"
    )



@bot.command()
async def ping(ctx):

    ms = round(
        bot.latency * 1000
    )


    await ctx.send(
        f"🏓 Pong! `{ms}ms`"
    )



# ==========================
# FEHLER AUSGABE
# ==========================

@bot.event
async def on_command_error(ctx, error):

    print(
        f"❌ Fehler: {error}"
    )



# ==========================
# BOT START
# ==========================

print("🚀 Bot startet...")


bot.run(TOKEN)