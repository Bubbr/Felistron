# TODO
# Trabajar con los usuarios, levels, ranking, economia, etc


import discord

from bot.config import meta
from bot.config import prefix
from bot.config import commands
from bot.config import token
from bot.util import react_mention

import bot.database as db

client  = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{prefix}help"))
    print(f"\nHola iniciando como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    await db.add_xp(message)

    if message.content.find(prefix) == 0:
        parse = message.content.split(' ')
        command = parse[0].split(prefix)[1]
        if not command in commands.keys():
            await message.channel.send(f":warning: El comando **{command}** no existe. Usa **f!help** para ver todos los comandos")
            return
        args = parse[1:]
        if command:
            for cmd in commands:
                if command == commands[cmd]["name"]:
                    if commands[cmd]['nsfw'] and not message.channel.is_nsfw():
                        await message.channel.send("No puedo mandar contenido nsfw en un canal family friendly")
                    else:
                        await commands[cmd]["func"].run(args, message, commands[cmd])
        else:
            await message.channel.send(meta["error"])
    elif message.mentions:
        if client.user in message.mentions:
            await react_mention(message)
            return

client.run(token)