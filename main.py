'''
main branch입니다 main branch는 수정하기 전 상의해주세요
'''
import discord,os
from discord.ext import commands
import bloomberg

#토큰
token_path = os.path.dirname( os.path.abspath( __file__ ) )+"/token.txt"
t = open(token_path,"r",encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ",token)

game = discord.Game("!도움")
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
cmd = {
	'도움': '무엇을 도와드릴까요?',
	'명령어': '가능한 명령어를 출력합니다.',
	'블룸버그': '오늘의 블룸버그 기사를 요약합니다.'
}

class Bloombutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)  # times out after 30 seconds
        button = discord.ui.Button(label='바로가기', style=discord.ButtonStyle.url, url="https://www.bloomberg.co.kr/blog/five-france-stock-optimism/")
        self.add_item(button)
        
    async def on_timeout(self):
        # set the view to None so that the buttons are no longer available
        # or you could just disable the buttons if you want
        await self.message.edit(content="링크가 종료되었습니다", view=None)
    
@bot.event
async def on_ready():
	print("안녕하세요 주식 정보를 알려주는 봇 Stocker입니다!")
    
@bot.command()
async def 도움(ctx):
	await ctx.send("무엇을 도와드릴까요?")

@bot.command()
async def 명령어(ctx):
	commands_list = '\n'.join([f"!{command}: {description}" for command, description in cmd.items()])
	await ctx.send(commands_list)

@bot.command()
async def 블룸버그(ctx):
	articles = bloomberg.getArticle()
	await ctx.send('\n'.join(articles))
	await ctx.send(view=Bloombutton())
bot.run(token)