import discord

from discord.message import Message

from bot.config import PREFIX
from bot.config import commands
from bot.config import TOKEN

from bot.util import react_mention
from bot.util import cmd_exists
from bot.util import not_found
from bot.util import NSFW_MESSAGE

import bot.database as db

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{PREFIX}help"))

#    for member in client.get_all_members():
#        if (db.user_exists(member.id)):
#            update = {
#                "$set": {
#                    "name": f"{member.name}#{member.discriminator}",
#                    "avatar_url": str(member.avatar_url)
#                }
#            }
#
#            #db.users.update_one({"uid": member.id}, update)
#
#    print(f"\nHola iniciando como {client.user}\n")


@client.event
async def on_message(message: Message):

    if message.author.bot:
        return

    await db.add_xp(message)

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
