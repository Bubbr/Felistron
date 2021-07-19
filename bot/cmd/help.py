from discord import Embed
from bot.util import color
from bot.util import commands
from bot.util import meta
from bot.util import prefix

async def run(args, ctx, acmd):
    if args:
        if not args[0] in commands.keys():
            await ctx.channel.send(f":warning: El comando **{args[0]}** no existe. Usa **f!help** para ver todos los comandos")
            return

        cmd = commands[args[0]]

        embed = Embed(
            title=f'Ayuda del comando {cmd["name"]}',
            description=cmd['description'],
            color=color
        )
        
        embed.add_field(
            name='Modo de uso',
            value=cmd['usage'].replace('{prefix}', prefix).replace('{name}', cmd['name'])
        )

        embed.add_field(
            name='Categoria',
            value=cmd['category']
        )

        embed.add_field(
            name='Alias',
            value=cmd['aliases']
        )

    else:
        embed = Embed(
            title='Centro de ayuda',
            color=color,
            description='Lista de todos los comandos del bot, utiliza el comando f!help <comando> para ver'
            +' informacion adicional.'
        )
        

        for category in meta["categories"]:
            cmds = ""
            for cmd in commands:
                if commands[cmd]['category'] == category:
                    cmds += f"``{commands[cmd]['name']}``   "
            embed.add_field(
                name=category,
                value=cmds
            )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )

    await ctx.channel.send(embed=embed)