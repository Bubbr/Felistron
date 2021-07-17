from pymongo import MongoClient
import pymongo
import json

from discord import Embed

from bot.util import color

meta     = json.load(open("db.json"))['database']

USERNAME = meta['user']['username']
PASSWORD = meta['user']['password']
DATABASE_NAME = meta['db_name']
CLUSTER_NAME = meta['cluster_name']

CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER_NAME}.x1tej.mongodb.net/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

db = client.get_database('store')

records = db.products

print("Base de datos iniciada")

async def shop(args, ctx, cmd):
    items = list(records.find())
    
    embed = Embed(
        title = 'Tienda',
        description = 'Compra todo lo que quieras',
        color = color
    )

    for item in items:
        embed.add_field(
            name=item['name'],
            value=f"Precio: ${item['price']}\nDescripcion: {item['description']}",
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

async def buy(args, ctx, cmd):
    await ctx.channel.send(cmd['name'])

command = {
    'shop': shop,
    'buy': buy
}

async def run(args, ctx, cmd):
    await ctx.channel.send("Comando disponible a partir de la version 1.0")
    await command[cmd['name']](args, ctx, cmd) 