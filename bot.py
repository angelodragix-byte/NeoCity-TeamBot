import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler


TOKEN = "MTUyMTUzNzU1MzQ1NzYxMDc1Mg.G5Z4sF.7dZtCVAlMhFaGU1qdnlswbW8mcl9e-JY3qOlas"

CHANNEL_ID = 1454908791647768798  # Schichtplan-Kanal

ROLE_PING = 1525222193976443053  # Rolle, die gepingt werden soll


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

scheduler = AsyncIOScheduler()


nachricht = """
**📅 Schichtplan**

<@&1525222193976443053>

Bitte tragt euch täglich in eine Schicht ein.
Wenn ihr euch nicht eintragt und euch auch nicht abmeldet, werden Teamwarns verteilt.

Pro Schicht sollen maximal fünf Leute dabei sein.

Wählt einfach die Schicht, die euch am besten passt:

🔴 **13:00 – 16:00**
🟠 **16:00 – 19:00**
🟡 **19:00 – 22:00**
🟢 **22:00 – 00:00**

Reagiert mit der passenden Emoji-Farbe.
"""


async def sende_schicht():

    kanal = bot.get_channel(CHANNEL_ID)

    if kanal:

        msg = await kanal.send(
            nachricht
        )

        for emoji in [
            "🔴",
            "🟠",
            "🟡",
            "🟢"
        ]:
            await msg.add_reaction(emoji)

        print("Schichtplan gesendet!")

    else:
        print("Kanal nicht gefunden!")


@bot.event
async def on_ready():

    print(f"{bot.user} ist online!")

    if not scheduler.running:

        scheduler.add_job(
            sende_schicht,
            "cron",
            hour=10,
            minute=00
        )

        scheduler.start()

        print("Schichtplan läuft jeden Tag um 10:00 Uhr")


@bot.command()
async def schicht(ctx):

    await sende_schicht()

    await ctx.send(
        "✅ Schichtplan wurde gesendet!"
    )


bot.run("MTUyMTUzNzU1MzQ1NzYxMDc1Mg.G5Z4sF.7dZtCVAlMhFaGU1qdnlswbW8mcl9e-JY3qOlas")