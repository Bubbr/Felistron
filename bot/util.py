import json
import random

import discord
from discord import Asset

meta    = json.load(open("bot.json"))

color   = int(meta["color"], 16)
prefix  = meta["prefix"]
mention = meta["mention"]

commands = meta["commands"]

with open('token.txt', 'r') as f:
    token = f.read()

async def load_img_asset(img_asset:Asset):
    import cv2
    import numpy as np

    asset = await img_asset.read()
    img_array = np.array(bytearray(asset), dtype=np.uint8)
    source = cv2.imdecode(img_array, -1)

    return source

def load_img_url(img_url:str):
    import cv2
    import numpy as np
    import urllib

    req = urllib.request.Request(img_url, headers={'User-Agent' : "Magic Browser"})
    con = urllib.request.urlopen( req )
    img_array = np.asarray(bytearray(con.read()), dtype=np.uint8)
    source = cv2.imdecode(img_array, -1)

    return source

def parser(content):
    parse = content.split(' ')
    command = parse[0].split(1)[1]
    args = parse[1:]

def custom_emoji(ctx, name):
    emojis = ctx.guild.emojis
    for emoji in emojis:
        if emoji.name == name:
            return emoji
    return None

async def react_mention(ctx, delete=False, delay=120):
    reaction = mention[random.randint(0, len(mention)-1)]

    if reaction["type"] == "reaction":
        emoji = custom_emoji(ctx, reaction["emoji"]["name"])
        await ctx.add_reaction(emoji)
        return

    if reaction["type"] == "generic":
        file = None
    elif reaction["type"] == "attachment":
        file = discord.File(reaction["attachment"])
    else:
        file = None

    if reaction["reply"]:
        msg = await ctx.reply(
            content=reaction["content"],
            file=file
        )
    else:
        msg = await ctx.channel.send(
            content=reaction["content"],
            file=file
        )
    if delete:
        await msg.delete(delay=delay)