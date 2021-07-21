from typing import Dict
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import requests
import discord
import io
import json

img_edit = json.load(open('img.json'))

def generic(source:Image, img_edit:Dict, parseable:Dict=None) -> Image:
    ed = img_edit
    images = ed['images']

    if images[0]['src']:
        base = Image.open(images[0]['src'])
    else:
        base = source
    
    if images[0]['resize']:
        if type(images[0]['resize']) is list:
            base = base.resize(tuple(images[0]['resize']))

        elif type(images[0]['resize']) is str:
            from_src = images[int(images[0]['resize'])]['src']

            if from_src:
                resize = Image.open(from_src).size

            else:
                resize = source.size

            base = base.resize(resize)

    for img in images[1:]:

        if img['src']:

            paste_img = Image.open(img['src'])

        else:
            paste_img = source
            
        if img['resize']:
            
            if type(img['resize']) is list:
                paste_img = paste_img.resize(tuple(img['resize']))

            elif type(img['resize']) is str:
                from_src = images[int(img['resize'])]['src']

                if from_src:
                    resize = Image.open(from_src).size

                else:
                    resize = source.size

                paste_img = paste_img.resize(resize)

        base.paste(
            paste_img,
            img['position'],
            paste_img.convert('RGBA')
        )
    
    if 'text' in ed.keys():
        draw = ImageDraw.Draw(base)
        
        for text in ed['text']:
            font = ImageFont.truetype(
                text['font'],
                text['size']
            )
            txt = text['text']

            if text['parse'] and parseable:
                for label in parseable:
                    txt = txt.replace(label, parseable[label])

            draw.text(
                tuple(text['position']),
                txt,
                tuple(text['color']),
                font=font
            )

    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    file = discord.File(io.BytesIO(img_byte_arr), filename=f'img.png')

    return file


async def run(args, ctx, cmd):
    type = img_edit[cmd['name']]['type']

    if type == 'generic':

        if args and ctx.mentions:
            img_url = ctx.mentions[0].avatar_url
        else:
            img_url = ctx.author.avatar_url
        
        source = Image.open(requests.get(img_url, stream=True).raw)

        file = generic(source, img_edit[cmd['name']])

    await ctx.channel.send(file=file)