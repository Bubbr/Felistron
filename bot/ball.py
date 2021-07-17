from discord import Embed
import random
from bot.util import color

wisdoms = [
    "No lo se",
    "Pregunta mas tarde",
    "Afirmativo",
    "Totalmente de acuerdo",
    "No",
    "Si"
]

async def run(args, ctx, cmd):
    embed = Embed(
        title=" ".join(args),
        description=f"**Respuesta:** {wisdoms[random.randint(0,len(wisdoms)-1)]}",
        color=color
    )
    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )
    await ctx.channel.send(embed=embed)