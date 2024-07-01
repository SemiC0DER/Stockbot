import discord

def embedMarket(market):
    current_color = 0xFF0000 if market[3][0] == '+' else 0x0100FF
    embed = discord.Embed(title=market[0], description='', color=current_color)
    embed.add_field(name=market[1], value='', inline=False)
    embed.add_field(name=market[2], value='', inline=False)
    embed.add_field(name=market[3], value='', inline=False)
    embed.set_image(url=market[4])
    return embed

def embedNews(article):
    today_article = discord.Embed(title=article[0], description=article[1], color=0x000000)
    today_article.set_image(url=article[2])
    return today_article

class linkbutton(discord.ui.View):
    def __init__(self, url):
        super().__init__(timeout=30)  # times out after 30 seconds
        button = discord.ui.Button(label='바로가기', style=discord.ButtonStyle.url, url=url)
        self.add_item(button)
        
    async def on_timeout(self):
        self.clear_items()


def embedStock(detail): #detail == [제목, 정보, 가격, 변화, 변화%, 시장상태, url]
    current_color = 0xFF0000 if detail[3][0] == '+' else 0x0100FF
    embed = discord.Embed(title=detail[0], description=detail[1], color=current_color)
    embed.set_thumbnail(url='https://i-invdn-com.investing.com/redesign/images/seo/investing_300X300.png')
    embed.add_field(name=detail[2], value='', inline=False)
    embed.add_field(name=detail[3], value='', inline=True)
    embed.add_field(name=detail[4], value='', inline=True)
    embed.set_footer(text=detail[5])
    button = linkbutton(detail[6])
    return [embed, button]