import discord
import cv2
import io
from bot.util import load_img_asset

async def run(args, ctx, cmd):
    if args:
        img_url = ctx.mentions[0].avatar_url
    else:
        img_url = ctx.author.avatar_url
    
    source = await load_img_asset(img_url)

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)

    img = cv2.imencode('.jpg', gray)[1]
    file = discord.File(io.BytesIO(img), filename='pto.jpg')

    await ctx.channel.send(file=file)