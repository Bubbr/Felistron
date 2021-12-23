from discord import Embed
from bot.util import color

async def run(args, ctx, cmd):
    guild = {
        'name': ctx.guild.name,
        'owner': ctx.guild.owner,
        'member_count': ctx.guild.member_count,
        'icon_url': ctx.guild.icon_url,
        'created_at': ctx.guild.created_at,
        'banner_url': ctx.guild.banner_url,
        'description': ctx.guild.description
    }

    embed = Embed(
        title=guild['name'],
        description= guild['description'] if guild['description'] else '' ,
        color=color
    )

    embed.set_thumbnail(url=guild['icon_url'])

    embed.add_field(
        name='Fue creado el',
        value=guild['created_at'].strftime('%Y-%m-%d'),
        inline=False
    )

    embed.add_field(
        name='Miembros',
        value=guild['member_count'],
        inline=False
    )

    embed.add_field(
        name='Owner',
        value=guild['owner'],
        inline=False
    )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )

    await ctx.channel.send(embed=embed)
