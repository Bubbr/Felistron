import random

RED = ":red_circle:"
YELLOW = ":yellow_circle:"
GREEN = ":green_circle:"

async def run(args, ctx, cmd):
    user = ctx.mentions[0] if len(ctx.mentions) > 0 else ctx.author
    
    random.seed(user.id)
    furryness = random.randint(0, 100)

    if (furryness >= 66):
        color = RED
    elif (furryness < 66 and furryness >= 33):
        color = YELLOW
    else:
        color = GREEN

    await ctx.channel.send(f"{color} {user.mention} es {furryness}% furro!")
