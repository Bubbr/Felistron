from pymongo import MongoClient
import pymongo
import json
import math
import random
import datetime

from discord import Embed

from bot.util import color
from bot.util import prefix

from bot.cmd.img import generic
from PIL import Image
import requests

meta     = json.load(open("db.json"))['database']
imd_edit = json.load(open("img.json"))

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

def upload_banner(source:Image, type:str):
    banner = {
        "type": "custom",
        "file": 1
    }

def give_item(quantiy, item_id=None, item_name=None):
    pass

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
        ],
        "daily": datetime.datetime.utcnow(),
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
        users.update_one(filter, {"$inc": {"balance": 50}})
        await ctx.channel.send(f"Felicidades {ctx.author.mention} acabas de subir al nivel {lvl}! "+
                                f"Y ganaste ${50}"
                                )

async def bet(args, ctx, cmd):
    if not args:
        await ctx.channel.send(
            "Debes especificar una cantidad a apostar y el numero al que apuestas\n"+
            f"Usa el comando {prefix}help {cmd['name']} para ver mas informacion"
            )
        return
    
    quantity = int(args[0])

    if len(args) < 2:
        await ctx.channel.send(
            "Debes especificar el numero al que apuestas (del 1 al 7)\n"+
            f"Usa el comando {prefix}help {cmd['name']} para ver mas informacion"
            )
        return

    
    number = int(args[1])

    if number < 1 or number > 7:
        await ctx.channel.send(
            "El numero debe ser entre el 1 y el 7\n"+
            f"Usa el comando {prefix}help {cmd['name']} para ver mas informacion"
            )
        return

    uid = ctx.author.id
    user = users.find_one({'uid': uid})
    user_balance = user['balance']

    if user_balance < quantity:
        await ctx.channel.send(
            "Lo siento pero parece que no tienes suficiente dinero en tu cuenta\n"+
            f"Te falta ${quantity-user_balance} para apostar\n"+
            "Puedes conseguir mas dinero vendiendo objetos, subiendo de nivel "+
            "o rogarle a otros usuarios que te presten un poco mas"
        )
        return
    
    lucia = random.randint(1, 7)

    if lucia == number:
        users.update_one({'uid': uid}, {"$inc": {"balance": quantity*2}})
        await ctx.channel.send(
            f"Tu numero: {number}\nNumero de la maquina: {lucia}\n\n"+
            f"Felicidades! Acabas de ganar ${quantity*2}\n"+
            f"Actualmente tienes ${user_balance+quantity*2} en tu cuenta!"
            )
    else:
        users.update_one({'uid': uid}, {"$inc": {"balance": -quantity}})
        await ctx.channel.send(
            f"Tu numero: {number}\nNumero de la maquina: {lucia}\n\n"+
            f"Lo siento, lamentablemente perdiste ${quantity}\n"+
            f"Actualmente tienes ${user_balance-quantity} en tu cuenta"
            )

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
    edit = imd_edit[cmd['name']]
    user = users.find_one({"uid": ctx.author.id})

    xp_to_next_level = int((2**(user['level'])-0.5)*10)

    parseable = {
        '{user.level}': str(user['level']),
        '{user.xp}': str(user['xp']),
        '{user.next_xp}': str(xp_to_next_level)
    }

    edit['images'][1]['resize'][0] = int(user['xp']/xp_to_next_level*edit['images'][1]['resize'][0])

    user_img = ctx.author.avatar_url

    source = Image.open(requests.get(user_img, stream=True).raw)

    file = generic(source, edit, parseable)

    await ctx.channel.send(file=file)

async def get_balance(args, ctx, cmd):
    uid = ctx.author.id
    balance = users.find_one({"uid": uid})['balance']

    await ctx.channel.send(
        f"Actualmente tienes ${balance} en tu cuenta"
    )

async def daily(args, ctx, cmd):
    uid = ctx.author.id
    user = users.find_one({'uid': uid})
    last_daily = user['daily']
    now = datetime.datetime.utcnow()

    delta_daily = now - last_daily

    if delta_daily.days >= 1:
        users.update_one({'uid': uid}, {'$set': {'daily': now}, '$inc': {'balance': 100}})
        await ctx.channel.send(
            f"Felicidades, acabas de reclamar tu recompensa diaria +${100}"
        )
    else:
        tomorrow = last_daily + datetime.timedelta(days=1)
        tomorrow_delta = tomorrow - now
        await ctx.channel.send(
            "Aun no puedes reclamar tu recompensa diaria, tienes que esperar "+
            f"{tomorrow_delta.seconds//3600}h {(tomorrow_delta.seconds//60)%60}m"
        )

command = {
    'shop': shop,
    'buy': buy,
    'level': get_level,
    'bet': bet,
    'balance': get_balance,
    'daily': daily
}

async def run(args, ctx, cmd):
    #await ctx.channel.send("Comando disponible a partir de la version 1.0")
    await command[cmd['name']](args, ctx, cmd) 