from discord import Embed
from discord.message import Message
import random
from bot.util import color

wisdoms = [
    "No lo sé",
    "Pregunta más tarde",
    "Totalmente de acuerdo",
    "No",
    "Si",
    "Tal vez",
    "No estoy seguro",
    "Confía en ello",
    "Tengo fe",
    "Lo que se ve no se pregunta",
    "Lo mismo me pregunto",
    "100% seguro",
    "Cuenta con ello"
]

async def run(args: list, ctx: Message, cmd: dict):
    embed = Embed(
            description=f"**Pregunta:** {' '.join(args)}\n\n**Respuesta:** {random.choice(wisdoms)}",
            color=color
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )
    await ctx.channel.send(embed=embed)
