from discord import Embed
from discord.message import Message
from bot.util import color

async def run(args: list, ctx: Message, cmd: dict) -> None:
    user = ctx.author if len(ctx.mentions) < 1 else ctx.mentions[0]

    embed = Embed(
        title=f'Avatar de {user.name}',
        color=color,
        description='Haz lo que quieras con la foto'
    )

    embed.set_image(
        url=user.avatar_url
    )

    await ctx.channel.send(embed=embed)
