from discord import Embed
import random
from bot.util import color

wisdoms = [
    "No lo se",
    "Pregunta mas tarde",
    "Totalmente de acuerdo",
    "No",
    "Si"
]

async def run(args, ctx, cmd):
    embed = Embed(
            description=f"**Pregunta:** {' '.join(args)}\n\n**Respuesta:** {random.choice(wisdoms)}",
            color=color
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )
    await ctx.channel.send(embed=embed)
