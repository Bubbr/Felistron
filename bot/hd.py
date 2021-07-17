import discord
import cv2
import io
from bot.util import load_img_asset, load_img_url

async def run(args, ctx, cmd):
    if args:
        img_asset = ctx.mentions[0].avatar_url
        source = await load_img_asset(img_asset)
    else:
        messages = await ctx.channel.history(limit=100).flatten()

        for msg in messages:
            if msg.attachments:
                img_url = msg.attachments[0].url
                break
        
        source = load_img_url(img_url)


    resized = cv2.resize(source, (int(source.shape[1]*0.05), int(source.shape[0]*0.05)))
    resized2 = cv2.resize(resized, (source.shape[1], source.shape[0]), interpolation=cv2.INTER_NEAREST)

    img = cv2.imencode('.jpg', resized2)[1]
    file = discord.File(io.BytesIO(img), filename='pto.jpg')

    await ctx.channel.send(file=file)