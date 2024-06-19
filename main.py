'''
main branch입니다 main branch는 수정하기 전 상의해주세요
'''
import discord,os
from discord.ext import commands
import Bloomberg
import DomesticMarket
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
    market = DomesticMarket.getDomesticMarket(1)
    kospi = MessageTools.embedMarket(market)
    await ctx.send(embed=kospi)

@bot.command()
async def 코스닥(ctx):
    market = DomesticMarket.getDomesticMarket(2)
    kosdaq = MessageTools.embedMarket(market)
    await ctx.send(embed=kosdaq)

@bot.command()
async def 코스피200(ctx):
    market = DomesticMarket.getDomesticMarket(3)
    kospi = MessageTools.embedMarket(market)
    await ctx.send(embed=kospi)

@bot.command()
async def 용어(ctx,*,text):
    meaning = StockDict.stockWord(text)
    page = discord.Embed(title=text, description=meaning, color=0x62c1cc)
    await ctx.send(embed=page)

bot.run(token)