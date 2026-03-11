import discord
from discord import app_commands, ChannelType, guild, ui
from discord.ui import View, Button, Select, Modal, TextInput
from discord.ext import commands, tasks
import os
import asyncio
import random
import re
import json
import requests
import time
from datetime import datetime, timedelta
import io
from discord.utils import utcnow
import math
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="+", intents=intents, help_command=None)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Systèmes synchronisés pour {self.user}")

bot = MyBot()

OWNER_IDS = [1447233337830936807, 1477344366769999913]


def is_team_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNER_IDS
    return commands.check(predicate)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online, 
        activity=discord.Game(name="dis-hub.github.io")
    )
    print('Le bot est prêt !')

@bot.command()
@is_team_owner()
async def statut(ctx, mode: str, *, texte: str = None):
    mode = mode.lower()
    
    status_map = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "invisible": discord.Status.invisible,
        "live": discord.Status.online
    }

    new_status = status_map.get(mode, discord.Status.online)
    
    activity = None
    if texte:
        if mode == "live":
            activity = discord.Streaming(name=texte, url="https://www.twitch.tv/discord")
        else:
            activity = discord.Game(name=texte)


    await bot.change_presence(status=new_status, activity=activity)
    
    if texte:
        message_confirm = f"Statut **{mode}** défini avec : *{texte}*"
    else:
        message_confirm = f"Statut **{mode}** défini."
        
    await ctx.send(message_confirm)




@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Latence: `{latency}ms`")






@bot.command()
@is_team_owner()
async def regle(ctx):
    embed = discord.Embed(
        title="*DISCORD HUB | SERVER RULES*",
        url="https://dis-hub.github.io/",
        description="**1. General Conduct**\n> `-` **Respect is Key** : Treat all members, staff, and guests with respect. No hate speech, racism, sexism, or harassment will be tolerated.\n\n> `-` **No Toxicity** : Avoid arguments, drama, or provocative behavior. If you have a conflict, take it to DMs or contact a Moderator.\n\n> `-` **Language** : Please use English or French in all public channels to ensure everyone can understand and participate.\n\n**2. Chat & Content**\n> `-` **No Spamming** : Do not flood the chat with symbols, emojis, caps, or repetitive messages.\n\n> `-` **Right Channel** : Use the appropriate channels for their intended purpose. (Check the channel descriptions!)\n\n> `-` **No NSFW** : This is a SFW (Safe For Work) server. No adult content, gore, or suggestive material is allowed.\n\n> `-` **External Links** : Do not post suspicious links, screamers, or any form of malware.\n\n**3. Advertising & Promotion**\n> `-` **No Self-Promotion** : Do not DM members or post invite links/advertisements without official partnership or permission from the Staff.\n\n> `-` **No Begging** : Do not ask for Nitro, roles, or money.\n\n**4. Enforcement**\n> `-` **Follow Discord ToS** : You must comply with the [Discord Community Guidelines](https://discord.com/guidelines)\n\n> `-` **Staff Authority** : The Staff team has the final say in all matters. Bypassing a mute or ban with an alt account will result in a permanent ban.\n\n**Need Assistance?**\nIf you have questions or need to report a member, please head over to <#1480830542311198730>",
        color=0x5865F2
    )

    await ctx.send(embed=embed)

@bot.command()
async def test(ctx):
    await ctx.send("Test")


bot.run(os.getenv('DISCORD_TOKEN'))