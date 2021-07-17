async def run(args, ctx, cmd):
    await ctx.channel.send(" ".join(args))
    await ctx.delete()