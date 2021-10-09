from typing import Dict
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import cv2
import numpy as np
import requests
import discord
import io
import json

aaa = json.load(open('img.json'))

def sepia(src_image):
    gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    #solid color
    sepia = np.ones(src_image.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    return np.array(sepia, np.uint8)

def generic(source:Image, img_edit:Dict, parseable:Dict=None) -> Image:
    edit = img_edit
    images = edit['images']

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

        #if img['rotation']:
        #    paste_img.rotate(img['rotate'])

        if 'mask' in img:
            #print(img['mask'])
            mask = Image.open(img['mask']).convert('L')
        else:
            mask = paste_img.convert('RGBA')

        base.paste(
            paste_img,
            img['position'],
            mask=mask
        )
    
    if 'text' in edit.keys():
        draw = ImageDraw.Draw(base)
        
        for text in edit['text']:
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
    type = aaa[cmd['name']]['type']

    if type == 'generic':

        if args and ctx.mentions:
            img_url = ctx.mentions[0].avatar_url
        else:
            img_url = ctx.author.avatar_url
        
        source = Image.open(requests.get(img_url, stream=True).raw)

        file = generic(source, aaa[cmd['name']])

    await ctx.channel.send(file=file)