'''
봇이 명령어를 받는 공간입니다
'''
import discord,os
from discord import app_commands
from discord.ext import commands
import Ap
import Bloomberg
import StockMarket
import MessageTools
import StockDict
from dotenv import load_dotenv

#토큰 로드
load_dotenv()

#봇 생성
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
game = discord.Game("/도움")
cmd = {
	'/도움': '무엇을 도와드릴까요?',
	'/블룸버그': '오늘의 블룸버그 기사를 요약합니다.',
    '/증시': '(/증시 \"찾을 증시\")로 현재시각의 증시를 보여줍니다. (/증시목록으로 종류를 보여줍니다)',
    '/증시목록': '/증시 명령어로 보여줄 수 있는 주식시장의 목록을 보여줍니다.',
    '/용어': '(/용어 \"찾을 용어\")로 주식 용어를 보여줍니다. (/용어목록으로 용어들을 보여줍니다.)',
    '/용어목록': '등재된 용어들의 목록을 보여줍니다.'
}
    
@bot.event
async def on_ready():
	print("안녕하세요, 주식 정보를 알려주는 봇 Stocker입니다!")
    
@bot.tree.command(name="도움", description=cmd['/도움'])
async def 도움(ctx):
    commands_list = '\n\n'.join([f"{command}: {description}" for command, description in cmd.items()])
    help = discord.Embed(
        title='도움말',
        description=commands_list,
        color=0xffc0cb
    )
    await ctx.response.send_message(embed=help)

'''
@bot.slash_command(name="AP", description=cmd['/AP'])
async def AP(ctx):
    articles = Ap.getArticle()
    today_articles = discord.Embed(title=articles[0], description=articles[1], color=0x000000)
    today_articles.set_image(url=articles[2])
    button = MessageTools.linkbutton(articles[3])
    await ctx.send(embed=today_articles)
    await ctx.send(view=button)
'''
@bot.tree.command(name="블룸버그", description=cmd['/블룸버그'])
async def 블룸버그(ctx: discord.Interaction):
    try:
        # 인터랙션 응답 시간을 늘리기 위해 defer 사용
        await ctx.response.defer(thinking=True)
        
        # 기사 가져오기
        articles = Bloomberg.getArticle()
        today_articles = discord.Embed(title=articles[0], description=articles[1], color=0xffc0cb)
        today_articles.set_image(url=articles[2])
        
        # 링크 버튼 생성
        button = MessageTools.linkbutton(articles[3])
        
        # 응답 메시지 전송
        await ctx.followup.send(embed=today_articles, view=button)
        
    except Exception as e:
        # 예외 발생 시 메시지 전송 및 로그 출력
        await ctx.followup.send("명령어를 실행하는 동안 오류가 발생했습니다.")
        print(f"Error: {e}")

@bot.tree.command(name="증시", description=cmd['/증시'])
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
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message('그런 주식시장이 등록되지 않았습니다. 가능한 시장을 /증시목록으로 확인해주세요')
    else:
        await ctx.response.send_message("찾을 주식시장을 입력해주세요.")

@bot.tree.command(name="증시목록", description=cmd['/증시목록'])
async def 증시목록(ctx):
    markets = list(StockMarket.getMarketAll())
    marketlist = discord.Embed(title='증시목록', description='\n'.join(markets), color=0xED0086)
    await ctx.response.send_message(embed=marketlist)

@bot.tree.command(name="용어", description=cmd['/용어'])
@app_commands.describe(text="검색할 주식 용어를 입력하세요.")
async def 용어(ctx,*,text : str = None):
    if text:
        meaning = StockDict.stockWord(text)
        page = discord.Embed(title=text, description=meaning, color=0x62c1cc)
        await ctx.response.send_message(embed=page)
    else:
        await ctx.response.send_message("찾을 용어를 입력해주세요.")

@bot.tree.command(name="용어목록", description=cmd['/용어목록'])
async def 용어목록(ctx):
    wordlist = StockDict.wordList()
    book = discord.Embed(title='용어목록', description=wordlist, color=0x62c1cc)
    await ctx.response.send_message(embed=book)

bot.run(os.getenv('TOKEN'))