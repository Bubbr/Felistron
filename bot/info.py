from discord import Embed
from bot.util import color
from bot.util import meta

async def run(args, ctx, cmd):
    embed = Embed(
        description='Informacion del bot',
        color=color
    )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )

    embed.add_field(
        name='Version',
        value=meta['version']
    )

    embed.add_field(
        name='Creador',
        value=meta['creator']
    )
    
    embed.add_field(
        name='Prefix',
        value=meta['prefix']
    )

    embed.set_thumbnail(
        url=meta['avatar_url']
    )

    await ctx.channel.send(embed=embed)