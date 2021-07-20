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
    tags = soup.find_all('span', attrs={'class': 'tags'})

    embed = Embed(
        title=sauce,
        url=url,
        color=color
    )

    tag_names = ""

    for tag in tags:
        name = tag.find('span', attrs={'class', 'name'})

        if name:
            tag_url = tag.a['href']
            tag_names += f" [{name.contents[0]}]({LINK}{tag_url}) |"

    embed.set_image(url=img_url)

    embed.add_field(
        name='Tags',
        value=tag_names
    )

    await ctx.channel.send(embed=embed)