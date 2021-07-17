from PIL import Image
import requests
import discord
import io
import json

img_edit = json.load(open('img_edit.json'))

def edit(source, cmd):
    ed = img_edit[cmd['name']]
    bg = Image.open(ed['bg']) 

    if ed['source']['resize']:
        source = source.resize(tuple(ed['source']['resize']))

    img = Image.open(ed['img']['src'])

    bg.paste(source, tuple(ed['source']['position']), source.convert('RGBA'))

    bg.paste(img, tuple(ed['img']['position']), img.convert('RGBA'))

    img_byte_arr = io.BytesIO()
    bg.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    file = discord.File(io.BytesIO(img_byte_arr), filename='bonk.png')

    return file

async def run(args, ctx, cmd):
    if args:
        img_url = ctx.mentions[0].avatar_url
    else:
        img_url = ctx.author.avatar_url
    
    source = Image.open(requests.get(img_url, stream=True).raw)

    file = edit(source, cmd)

    await ctx.channel.send(file=file)