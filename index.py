import discord
from discord.ext import commands
import time
import random
import asyncio
from collections import defaultdict
from profanity_check import predict, predict_prob
import os
#봇의 설정
prefix = "~"  # 봇의 명령어 접두사
intents = discord.Intents.all()  #모든 intents를 활성화

#봇 생성
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    lt = time.localtime(time.time())
    print(time.strftime('%Y-%m-%d %H:%M:%S', lt))


# 봇의 설정
prefix = "~"  # 봇의 명령어 접두사
intents = discord.Intents.all()  # 모든 intents를 활성화

# 봇 생성
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    lt = time.localtime(time.time())
    print(time.strftime('%Y-%m-%d %H:%M:%S', lt))
    print('서비스 준비 완료')
    print('봇 이름: {0}!'.format(bot.user))
    # 봇이 시작될 때 돈 정보와 역할 상점 정보를 파일에서 불러옴
    # 프리센스 메시지의 리스트
    presences = ["커뮤니티의 보안을 이 봇으로 지켜보세요!", "성능 좋은 보안 봇이에요!"]
    # 이전 프리센스를 저장하는 변수
    prev_presence = None

    # 봇의 프리센스를 변경하는 루프
    async def update_presence():
        nonlocal prev_presence  # 외부의 prev_presence 변수 사용

        while True:
            # 랜덤으로 프리센스 메시지 선택
            presence_message = random.choice(presences)

            # 이전 프리센스와 같으면 다시 랜덤한 프리센스 선택
            while presence_message == prev_presence:
                presence_message = random.choice(presences)

            # 봇의 프리센스 설정
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(presence_message))

            # 프리센스 변경 로그 출력
            print("로그 |", f'프리센스가 변경되었습니다. 새로운 프리센스: {presence_message}')

            # 현재 프리센스를 이전 프리센스로 저장
            prev_presence = presence_message

            # 20초 동안 기다린 후 프리센스를 다시 변경
            await asyncio.sleep(20)

    # 봇의 프리센스를 변경하는 루프를 백그라운드 태스크로 등록
    bot.loop.create_task(update_presence())
# 메시지 도배 감지를 위한 변수 설정
detection_interval = 10  # 도배 감지 주기(초)
max_messages = 8  # 허용되는 최대 도배 메시지 수
detection_threshold = 7  # 도배로 감지되는 횟수

# 감지된 도배 메시지를 저장하는 딕셔너리
flood_dict = defaultdict(int)

@bot.event
async def on_message(message):
    # 봇 메시지는 무시
    if message.author.bot:
        return

    # 감지된 도배 메시지를 저장하고 갱신
    flood_dict[message.author.id] += 1

    # 일정 주기마다 도배 메시지를 초기화
    await asyncio.sleep(detection_interval)
    flood_dict[message.author.id] = 0

    # 도배로 감지된 경우
    if flood_dict[message.author.id] >= detection_threshold:
        # 도배 메시지 삭제
        await message.delete()

        # 유저에게 안내 임베드 전송
        embed = discord.Embed(
            title="도배 감지",
            description=f"{message.author.mention},도배로 인해 메시지가 삭제되었습니다.",
            color=discord.Color.red()
        )
        await message.author.send(embed=embed)

        # 일정 시간이 지난 후 안내 임베드 삭제
        await asyncio.sleep(5)
        async for entry in message.author.history(limit=1):
            await entry.delete()


@bot.event
async def on_message(message):
    # 봇 메시지는 무시
    if message.author.bot:
        return

    # 욕설이 포함된 메시지인지 확인
    is_profane = predict([message.content])[0]

    if is_profane:
        # 욕설이 감지되면 메시지 삭제
        await message.delete()

        # 유저에게 욕설 감지 안내 임베드 전송
        embed = discord.Embed(
            title="욕설 감지",
            description=f"{message.author.mention}, 욕설이 감지되어 메시지가 삭제되었습니다.",
            color=discord.Color.red()
        )
        notification_message = await message.author.send(embed=embed)

        # 5초 후 안내 메시지 삭제
        await asyncio.sleep(5)
        await notification_message.delete()

    await bot.process_commands(message)

access_token.eviron["BOT_TOKEN"]

#봇을 실행
bot.run('access_token')
