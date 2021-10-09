import discord
import re

from bot.config import PREFIX
from bot.config import commands
from bot.config import TOKEN

from bot.util import react_mention
from bot.util import cmd_exists
from bot.util import not_found
from bot.util import NSFW_MESSAGE

import bot.database as db

client  = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{PREFIX}help"))
    print(f"\nHola iniciando como {client.user}\n")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await db.add_xp(message)

    if (message.channel.id == 809626508674072577):
        count_buffer = 0

        async for msg in message.channel.history(limit=10):
            count = int(re.match(r'^([\s\d]+)$', msg.content.split(' ')[0]).group(0))

            if (count_buffer == 0):
                count_buffer = count
                continue

            if (count_buffer - count) != 1:
                reply = await message.reply("Seguro sabes contar? :face_with_raised_eyebrow:")
                await reply.delete(delay=10)
                await message.delete(delay=10)

            count_buffer = count

    if message.content.find(PREFIX) == 0:
        parse = message.content.split(' ')
        command = parse[0].split(PREFIX)[1]
        args = parse[1:]
        cmd = cmd_exists(command)

        if not cmd:
            await message.channel.send(await not_found(command))
            #await message.channel.send(f":warning: El comando **{command}** no existe. Usa **{PREFIX}help** para ver todos los comandos")
            return

        if commands[cmd]['nsfw'] and not message.channel.is_nsfw():
            await message.channel.send(NSFW_MESSAGE)
            #await message.channel.send("No puedo mandar contenido nsfw en un canal family friendly")
            return

        await commands[cmd]["func"].run(args, message, commands[cmd])

    elif message.mentions:
        if client.user in message.mentions:
            await react_mention(message)
            return

if __name__ == "__main__":
    client.run(TOKEN)
