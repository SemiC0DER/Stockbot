'''
봇이 명령어를 받는 공간입니다
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
    '!증시': '(!증시 \"찾을 증시\)"로 현재시각의 증시를 보여줍니다. (!증시목록으로 종류를 보여줍니다)',
    '!증시목록': '!증시 명령어로 보여줄 수 있는 주식시장의 목록을 보여줍니다.',
    '!용어': '(!용어 \"찾을 용어\")로 주식 용어를 보여줍니다. (!용어목록으로 용어들을 보여줍니다.)',
    '!용어목록': '등재된 용어들의 목록을 보여줍니다.'
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
    today_articles = discord.Embed(title=articles[0], description='\n'.join(articles[1:]), color=0xffc0cb)
    await ctx.send(embed=today_articles)
    await ctx.send(view=button)

@bot.command()
async def 증시(ctx,*,message: str = None):
    if message:
        markets = StockMarket.getMarketAll()
        if message in markets:
            midx = markets[message]

            if midx <= 3:
                market = StockMarket.getDomesticMarket(midx)
            elif 3 < midx <= 12:
                market = StockMarket.getWorldMarket(midx-4)

            embed = MessageTools.embedMarket(market)
            await ctx.send(embed=embed)
        else:
            await ctx.send('그런 주식시장이 등록되지 않았습니다. 가능한 시장을 !증시목록으로 확인해주세요')
    else:
        await ctx.send("찾을 주식시장을 입력해주세요")

@bot.command()
async def 증시목록(ctx):
    markets = list(StockMarket.getMarketAll())
    marketlist = discord.Embed(title='증시목록', description='\n'.join(markets), color=0xED0086)
    await ctx.send(embed=marketlist)

@bot.command()
async def 용어(ctx,*,text : str = None):
    if text:
        meaning = StockDict.stockWord(text)
        page = discord.Embed(title=text, description=meaning, color=0x62c1cc)
        await ctx.send(embed=page)
    else:
        await ctx.send("찾을 용어를 입력해주세요")

@bot.command()
async def 용어목록(ctx):
    wordlist = StockDict.wordList()
    book = discord.Embed(title='용어목록', description=wordlist, color=0x62c1cc)
    await ctx.send(embed=book)

bot.run(token)