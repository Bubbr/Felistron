from dns.resolver import query
from pymongo import MongoClient
import pymongo
import json
import math

from discord import Embed

from bot.util import color

meta     = json.load(open("db.json"))['database']

USERNAME = meta['user']['username']
PASSWORD = meta['user']['password']
DATABASE_NAME = meta['db_name']
CLUSTER_NAME = meta['cluster_name']

CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER_NAME}.x1tej.mongodb.net/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

products = client.get_database('store').products
users = client.get_database('users').data
guilds = client.get_database('guilds').config

print("Base de datos iniciada")

def user_exists(uid):
    query = {'uid': uid}
    data = users.find(query)

    if data.count() > 0:
        data.close()
        return True
    else:
        data.close()
        return False

def register_user(uid):
    user = {
        "uid": uid,
        "xp": 0,
        "balance": 100,
        "level": 0,
        "items": [
            {
                "id": products.find_one({"name": "Soap"})['_id'],
                "quantity": 1
            }
        ]
    }

    r = users.insert_one(user)

    return r.inserted_id

async def add_xp(ctx):
    uid = ctx.author.id

    if user_exists(uid):
        uuid = users.find_one({"uid": uid})['_id']
    else:
        uuid = register_user(uid)
    
    filter = {"_id": uuid}
    users.update_one(filter, {"$inc": {"xp": 1}})

    xp = users.find_one({"_id": uuid})['xp']
    old_lvl = users.find_one({"_id": uuid})['level']

    lvl = math.floor(math.log2(xp/10 + 0.5) + 1)

    if lvl > old_lvl:
        users.update_one(filter, {"$set": {"level": lvl}})
        await ctx.channel.send(f"Felicidades {ctx.author.mention} acabas de subir al nivel {lvl}!")

async def shop(args, ctx, cmd):
    items = list(products.find())
    
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

async def get_level(args, ctx, cmd):
    user = users.find_one({"uid": ctx.author.id})
    
    embed = Embed(
        color = color
    )

    embed.add_field(
        name = 'Nivel',
        value = user['level']
    )

    embed.add_field(
        name = 'XP',
        value = user['xp']
    )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )

    await ctx.channel.send(embed=embed)

command = {
    'shop': shop,
    'buy': buy,
    'level': get_level
}

async def run(args, ctx, cmd):
    await ctx.channel.send("Comando disponible a partir de la version 1.0")
    await command[cmd['name']](args, ctx, cmd) 