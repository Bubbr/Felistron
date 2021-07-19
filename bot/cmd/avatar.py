from discord import Embed
from bot.util import color

async def run(args, ctx, cmd):
    embed = Embed(
        title=f'Avatar de {ctx.mentions[0].name}',
        color=color,
        description='Haz lo que quieras con la foto c:'
    )

    embed.set_image(
        url=ctx.mentions[0].avatar_url
    )

    await ctx.channel.send(embed=embed)