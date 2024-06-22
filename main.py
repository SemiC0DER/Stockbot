import discord
import os
from discord import app_commands
import Ap
import Bloomberg
import News
import StockMarket
import MessageTools
import StockDict
from dotenv import load_dotenv

# 토큰 로드
load_dotenv()

# 클라이언트 생성
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)
    
    async def on_ready(self):
        print(f'안녕하세요, 주식 정보를 알려주는 봇 Stocker입니다! {self.user}')
        await self.tree.sync()

client = MyClient()

cmd = {
    '/도움': '무엇을 도와드릴까요?',
    '/블룸버그': '오늘의 블룸버그 기사를 요약합니다.',
    '/뉴스': '(뉴스 "언론사")로 메이저 언론사의 최신 주식 뉴스를 보여줍니다. (/뉴스목록으로 종류를 보여줍니다)',
    '/뉴스목록': '/뉴스 명령어로 보여줄 수 있는 언론사들의 목록을 보여줍니다.',
    '/증시': '(/증시 "찾을 증시")로 현재시각의 증시를 보여줍니다. (/증시목록으로 종류를 보여줍니다)',
    '/증시목록': '/증시 명령어로 보여줄 수 있는 주식시장의 목록을 보여줍니다.',
    '/용어': '(/용어 "찾을 용어")로 주식 용어를 보여줍니다. (/용어목록으로 용어들을 보여줍니다.)',
    '/용어목록': '등재된 용어들의 목록을 보여줍니다.',
    '/ap': 'AP통신의 최신 주식시장 기사를 보여줍니다.'
}

@client.tree.command(name="도움", description=cmd['/도움'])
async def 도움(interaction: discord.Interaction):
    commands_list = '\n\n'.join([f"{command}: {description}" for command, description in cmd.items()])
    help_embed = discord.Embed(
        title='도움말',
        description=commands_list,
        color=0xffc0cb
    )
    await interaction.response.send_message(embed=help_embed)

@client.tree.command(name="뉴스", description=cmd['/뉴스'])
async def 뉴스(interaction: discord.Interaction,*,message : str = None):
    if message:
        available = News.classmap

        if message in available:
            try:
                news = available[message]
                article = news.getArticle()

                embed = MessageTools.embedNews(article)
                button = MessageTools.linkbutton(article[3])

                await interaction.followup.send(embed=embed, view=button)

            except Exception as e:
                await interaction.followup.send("명령어를 실행하는 동안 오류가 발생했습니다.")
                print(f"Error: {e}")
        else:
            interaction.response.send_message(f"{interaction.command}와 같은 언론사는 등록되지 않았습니다.\n\n\"!뉴스목록\"으로 가능한 뉴스를 찾으세요.")
    else:
        interaction.response.send_message("찾을 뉴스를 입력해주세요.")

@client.tree.command(name="뉴스목록", description=cmd['/뉴스목록'])
async def 뉴스목록(interaction: discord.Interaction):
    newslist = sorted(News.classmap)
    embed = discord.Embed(title='뉴스목록', description='\n'.join(newslist), color=0xED0086)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="블룸버그", description=cmd['/블룸버그'])
async def 블룸버그(interaction: discord.Interaction):
    try:
        await interaction.response.defer(thinking=True)
        
        article = Bloomberg.getArticle()
        embed = MessageTools.embedNews(article)
        button = MessageTools.linkbutton(article[3])
        
        await interaction.followup.send(embed=embed, view=button)
        
    except Exception as e:
        await interaction.followup.send("명령어를 실행하는 동안 오류가 발생했습니다.")
        print(f"Error: {e}")

@client.tree.command(name='ap', description=cmd['/ap'])
async def ap(interaction: discord.Interaction):
    try:
        await interaction.response.defer(thinking=True)
        
        article = Ap.getArticle()
        embed = MessageTools.embedNews(article)
        button = MessageTools.linkbutton(article[3])
        
        await interaction.followup.send(embed=embed, view=button)
        
    except Exception as e:
        await interaction.followup.send("명령어를 실행하는 동안 오류가 발생했습니다.")
        print(f"Error: {e}")

@client.tree.command(name="증시", description=cmd['/증시'])
async def 증시(interaction: discord.Interaction, message: str = None):
    if message:
        markets = StockMarket.getMarketAll()
        if message in markets:
            midx = markets[message]

            if midx <= 3:
                market = StockMarket.getDomesticMarket(midx)
            elif 3 < midx <= 12:
                market = StockMarket.getWorldMarket(midx-4)

            embed = MessageTools.embedMarket(market)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message('그런 주식시장이 등록되지 않았습니다. 가능한 시장을 /증시목록으로 확인해주세요')
    else:
        await interaction.response.send_message("찾을 주식시장을 입력해주세요.")

@client.tree.command(name="증시목록", description=cmd['/증시목록'])
async def 증시목록(interaction: discord.Interaction):
    markets = list(StockMarket.getMarketAll())
    marketlist = discord.Embed(title='증시목록', description='\n'.join(markets), color=0xED0086)
    await interaction.response.send_message(embed=marketlist)

@client.tree.command(name="용어", description=cmd['/용어'])
@app_commands.describe(text="검색할 주식 용어를 입력하세요.")
async def 용어(interaction: discord.Interaction, text: str = None):
    if text:
        meaning = StockDict.stockWord(text)
        page = discord.Embed(title=text, description=meaning, color=0x62c1cc)
        await interaction.response.send_message(embed=page)
    else:
        await interaction.response.send_message("찾을 용어를 입력해주세요.")

@client.tree.command(name="용어목록", description=cmd['/용어목록'])
async def 용어목록(interaction: discord.Interaction):
    wordlist = StockDict.wordList()
    book = discord.Embed(title='용어목록', description=wordlist, color=0x62c1cc)
    await interaction.response.send_message(embed=book)

# 봇 실행
client.run(os.getenv('TOKEN'))
