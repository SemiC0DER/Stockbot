'''
main branch입니다 main branch는 수정하기 전 상의해주세요
'''
import discord,os
from discord.ext import commands
import Bloomberg
import StockMarket
import MessageTools
import StockDict

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
    '!코스피': '코스피 주가를 보여줍니다.',
    '!코스닥': '코스닥 주가를 보여줍니다.',
    '!코스피200': '코스피200 주가를 보여줍니다.',
    '!다우': '다우 산업 주가를 보여줍니다.',
    '!나스닥': '나스닥 종합 주가를 보여줍니다',
    '!SP': 'S&P 500 주가를 보여줍니다',
    '!니케이': '니케이 225 주가를 보여줍니다',
    '!상해': '상해종합 주가를 보여줍니다',
    '!항셍': '항셍 주가를 보여줍니다',
    '!영국': '영국 FTSE 100 주가를 보여줍니다',
    '!프랑스': '프랑스 CAC 40 주가를 보여줍니다',
    '!독일': '독일 DAX 주가를 보여줍니다',
    '!용어': '!용어 \{찾을 용어\}로 주식 용어를 보여줍니다.'
}
    
@bot.event
async def on_ready():
	print("안녕하세요 주식 정보를 알려주는 봇 Stocker입니다!")
    
@bot.command()
async def 도움(ctx):
    commands_list = '\n\n'.join([f"{command}: {description}" for command, description in cmd.items()])
    help = discord.Embed(title='도움말', description=commands_list, color=0xffc0cb)
    await ctx.send(embed=help)
	
@bot.command()
async def 블룸버그(ctx):
    articles = Bloomberg.getArticle()
    link = Bloomberg.getLink()
    button = MessageTools.linkbutton(link)
    await ctx.send('\n'.join(articles))
    await ctx.send(view=button)

@bot.command()
async def 코스피(ctx):
    market = StockMarket.getDomesticMarket(1)
    kospi = MessageTools.embedMarket(market)
    await ctx.send(embed=kospi)

@bot.command()
async def 코스닥(ctx):
    market = StockMarket.getDomesticMarket(2)
    kosdaq = MessageTools.embedMarket(market)
    await ctx.send(embed=kosdaq)

@bot.command()
async def 코스피200(ctx):
    market = StockMarket.getDomesticMarket(3)
    kospi200 = MessageTools.embedMarket(market)
    await ctx.send(embed=kospi200)

@bot.command()
async def 다우(ctx):
    world = StockMarket.getWorldMarket(0)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 니케이(ctx):
    world = StockMarket.getWorldMarket(1)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 영국(ctx):
    world = StockMarket.getWorldMarket(2)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 나스닥(ctx):
    world = StockMarket.getWorldMarket(3)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 상해(ctx):
    world = StockMarket.getWorldMarket(4)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 프랑스(ctx):
    world = StockMarket.getWorldMarket(5)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def SP(ctx):
    world = StockMarket.getWorldMarket(6)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 항셍(ctx):
    world = StockMarket.getWorldMarket(7)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 독일(ctx):
    world = StockMarket.getWorldMarket(8)
    worldembed = MessageTools.embedMarket(world)
    await ctx.send(embed=worldembed)

@bot.command()
async def 용어(ctx,*,text):
    meaning = StockDict.stockWord(text)
    page = discord.Embed(title=text, description=meaning, color=0x62c1cc)
    await ctx.send(embed=page)

bot.run(token)