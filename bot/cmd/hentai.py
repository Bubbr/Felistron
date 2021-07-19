import requests
from bs4 import BeautifulSoup
from discord import Embed
from bot.util import color

LINK = "https://nhentai.net"
RANDOM = "/random/"
CODE = "/g/"

def parse_code(url):
    return url.split('/g/')[1].split('/')[0]

async def run(args, ctx, cmd):
    if args:
        sauce = str(args[0])
        url = LINK+CODE+sauce
    else:
        request = requests.get(url=LINK+RANDOM)
        url = request.url
        sauce = parse_code(url)

    request = requests.get(url=url)

    src = request.content

    soup = BeautifulSoup(src, 'html.parser')

    results = soup.find('a', attrs={'href': f"{CODE}{sauce}/1/"})

    img_url = results.img['data-src']

    embed = Embed(
        title=sauce,
        url=url,
        color=color
    )

    embed.set_image(url=img_url)

    await ctx.channel.send(embed=embed)