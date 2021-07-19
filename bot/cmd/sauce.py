import requests
from bs4 import BeautifulSoup

from discord import Embed

from bot.util import color

async def run(args, ctx, cmd):
    messages = await ctx.channel.history(limit=100).flatten()

    for msg in messages:
        if msg.attachments:
            img_url = msg.attachments[0].url
            break
    
    request_url = f"https://saucenao.com/search.php?url={img_url}"
    
    request = requests.get(url=request_url)

    src = request.content

    soup = BeautifulSoup(src, 'html.parser')

    results = soup.find_all('table', attrs={'class':'resulttable'})

    #result_img = results[0].find('div', attrs={'class':'resultimage'}).a.img.attrs['src']

    result_title    = results[0].find('div', attrs={'class':'resulttitle'}).strong.contents[0]
    result_content  = results[0].find('div', attrs={'class':'resultcontentcolumn'})

    content = []

    try:

        for i, child in enumerate(result_content.children):
            if child.name == "strong":
                content.append(
                    {
                        "key": child.contents[0].split(':')[0],
                        "value": list(result_content.children)[i+1].contents[0],
                        "url": list(result_content.children)[i+1].attrs['href']
                    }
                )

    except AttributeError:
        embed = Embed(
            title='Ocurrio un error',
            description=f'Ver resultados [web]({request_url})',
            color=0xff0000
        )

        embed.set_image(url=img_url)

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )
        embed.set_footer(
            text=f'Solicitado por {ctx.author.display_name}'
        )
        
        await ctx.channel.send(embed=embed)
        return
    
    embed = Embed(
        title= result_title,
        color= color
    )

    for field in content:
        embed.add_field(
            name=field['key'],
            value=f"[{field['value']}]({field['url']})"
        )
    

    embed.set_image(url=img_url)

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed.set_footer(
        text=f'Solicitado por {ctx.author.display_name}'
    )

    await ctx.channel.send(embed=embed)