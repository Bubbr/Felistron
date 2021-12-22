from discord.message import Message
from datetime import datetime

async def run(args, ctx: Message, cmd):

    start = ctx.created_at.utcnow().microsecond
    final = datetime.now().utcnow().microsecond

    ping = final - start

    await ctx.channel.send(f"Pong! :ping_pong: {ping}ms")