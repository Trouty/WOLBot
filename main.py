import os

import disnake
import wakeonlan
from disnake.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.environ["BOT_TOKEN"]
AUTH_ID = os.environ["AUTH_ID"]
COMPUTER_MACADDR = os.environ["COMPUTER_MACADDR"]

bot = commands.InteractionBot()
now = datetime.now()

@bot.event
async def on_ready():
    print("[INFO] Bot has finished init")

@bot.slash_command()
async def wakeup(interaction: disnake.CommandInteraction):
    current_timedate = now.strftime("%d/%m/%Y %H:%M:%S")

    if interaction.author.id != int(AUTH_ID):
        print(f"[WARN] {interaction.author.name} tried to send a WOL packet at {current_timedate} with the id {interaction.author.id}")

        return await interaction.response.send_message(f"You are not authorized to use this command")

    try:
        wakeonlan.send_magic_packet(COMPUTER_MACADDR)

        print(f"[INFO] WOL packet sent at {current_timedate} by {interaction.author.name} with the id {interaction.author.id}")

        await interaction.response.send_message(f"Wake packet sent to `{COMPUTER_MACADDR}`")
    except:
        print(f"[WARN] Attempted to send WOL packet  at {current_timedate} by {interaction.author.name} with the id {interaction.author.id}")

        await interaction.response.send_message("An error has occurred, try again later")

bot.run(TOKEN)