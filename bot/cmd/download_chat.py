"""
This command downloads the full channel history and send it as a .json file.
Usage: prefix!dchat [limit=100]
"""

import json
import io

import discord

async def run(args, ctx, cmd):

    limit = None

    if (len(args) > 0):
        try:
            limit = int(args[0])
        except ValueError as err:
            await ctx.channel.send(err)

    messages = await ctx.channel.history(limit=limit).flatten()

    data = {
            "messages": []
            }

    for msg in messages:
        idk = {
                "id": msg.id,
                "channel": {
                    "id": msg.channel.id,
                    "name": msg.channel.name
                    },
                "author": msg.author.id,
                "content": msg.content
                }

        data["messages"].append(idk)

    data1 = {
            "id": int,
            "channel": {
                "id": int,
                "name": str,
                "position": int,
                "nsfw": bool,
                "news": bool,
                "categor_id": int
            },
            "type": 10,#,MessageType,
            "author": 10,#Member,
            "flags": 10,#MessageFlags
    }

    raw = json.dumps(data, indent=4)

    filejson = discord.File(io.BytesIO(raw.encode()), filename="data.json")
    
    await ctx.channel.send(file=filejson)
