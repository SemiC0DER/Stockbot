'''
main branch입니다 main branch는 수정하기 전 상의해주세요
'''
import discord,os
from discord.ext import commands
import bloomberg
import stockmarket
#토큰
token_path = os.path.dirname( os.path.abspath( __file__ ) )+"/token.txt"
t = open(token_path,"r",encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ",token)

game = discord.Game("!도움")
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
cmd = {
	'!도움': '무엇을 도와드릴까요?',
	'!블룸버그': '오늘의 블룸버그 기사를 요약합니다.',
    '!증시': '오늘의 증시를 보여줍니다'
}

class Bloombutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)  # times out after 30 seconds
        button = discord.ui.Button(label='바로가기', style=discord.ButtonStyle.url, url=bloomberg.getLink())
        self.add_item(button)
        
    async def on_timeout(self):
        self.clear_items()

def embedMarket(n):
    market = stockmarket.getDomesticMarket(n)
    current_color = 0xFF0000 if market[3][0] == '+' else 0x0100FF
    embed = discord.Embed(title=market[0], description=market[1], color=current_color)
    embed.add_field(name=market[2], value=market[3], inline=False)
    embed.set_thumbnail(url=market[4])
    return embed
    
@bot.event
async def on_ready():
	print("안녕하세요 주식 정보를 알려주는 봇 Stocker입니다!")
    
@bot.command()
async def 도움(ctx):
	commands_list = '\n'.join([f"{command}: {description}" for command, description in cmd.items()])
	await ctx.send(commands_list)

@bot.command()
async def 블룸버그(ctx):
	articles = bloomberg.getArticle()
	await ctx.send('\n'.join(articles))
	await ctx.send(view=Bloombutton())

@bot.command()
async def 증시(ctx):
    kospi = embedMarket(1)
    await ctx.channel.send(embed=kospi)

    kosdaq = embedMarket(2)
    await ctx.channel.send(embed=kosdaq)

    kospi200 = embedMarket(3)
    await ctx.channel.send(embed=kospi200)

bot.run(token)