import random
import requests
from bs4 import BeautifulSoup
from discord import Embed
from bot.util import color

LINK = "https://nhentai.net"
RANDOM = "/random/"
CODE = "/g/"


def parse_code(url):
    return url.split('/g/')[1].split('/')[0]

def search(args):
    # GRACIAS A TacoAnime69 https://github.com/TacoAnime69
    # 
    # por compartir su codigo para que yo lo pueda copiar
    #
    # en realidad no es copy paste, solo tome su idea y lo implemente a mi modo
    #  
    # link a tu trabajo: https://github.com/TacoAnime69/RandomNhentai

    search_queue = 'https://nhentai.net/search/?q='
    #print()
    for i, tag in enumerate(args):
        temp = tag

        if ':' in temp:
            temp = tag.replace(':', '%3A')

        search_queue += temp

        if i != (len(args) - 1):
            search_queue += '+'

    #print(search_queue)

    page = requests.get(search_queue)

    #print(page.status_code)
    
    src = page.content

    soup = BeautifulSoup(src, 'html.parser')

    result = soup.find_all('div', attrs={'class': 'gallery'})

    if not result:
        return None

    last_page = soup.find('a', attrs={'class': 'last'})['href']
    last_page = int(last_page.split('&page=')[1])

    random_page = random.randint(1, last_page)
    random_url = f"{search_queue}&page={random_page}"

    #print(random_url)

    page = requests.get(random_url).content

    soup = BeautifulSoup(page, 'html.parser')

    covers = soup.find_all('a', attrs={'class': 'cover'})
    codes = []

    for cover in covers:
        codes.append(
            parse_code(cover['href'])
        )

    random_doujin = codes[random.randint(0, len(codes)-1)]

    #print(random_doujin)

    return str(random_doujin)

async def run(args, ctx, cmd):
    if args:
        try:
            int(args[0])
            sauce = str(args[0])

        except ValueError:            
            sauce = search(args)

            if not sauce:
                await ctx.channel.send("No se encontraron resultados")
                return
        
        url = LINK+CODE+sauce
    else:
        request = requests.get(url=LINK+RANDOM)
        url = request.url
        sauce = parse_code(url)

    #print(url)

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

    tag_names = []

    for tag in tags:
        name = tag.find('span', attrs={'class', 'name'})

        if name:
            tag_url = tag.a['href']
            tag_names.append(f"[{name.contents[0]}]({LINK}{tag_url})")

    embed.set_image(url=img_url)

    embed.add_field(
        name='Tags',
        value=" | ".join(tag_names[:-1])
    )

    await ctx.channel.send(embed=embed)