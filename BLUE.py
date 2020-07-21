import asyncio
import os

import discord
from discord.ext import commands
import datetime
import random
import time

app = commands.Bot(command_prefix='/')
app.remove_command("help")

access_token = os.environ["BOT_TOKEN"]
tokn = 'NzM0Njc4NTI1NDYxOTIxODM1.XxVMvw.nq7CeMwXxFxqvN1EcIjS5a_t79E'

@app.event
async def on_ready():
    print("==========")

@commands.has_role("인증 도움이 관리자권한")
@app.command(name="인증해체", pass_context=True)
async def 인증해체(ctx, user_name: discord.Member):
    if (str(ctx.guild) == "None"):
        emoji = ["이 명령어는 DM에서 사용을 못해요!", "디스코드 서버에서 사용해주세요!"]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))
    else:
        author = ctx.guild.get_member(int(user_name.id))
        await author.edit(nick="")
        role = discord.utils.get(ctx.guild.roles, name="[✅] 인증유저")
        await author.remove_roles(role)
        emoji = ["{}님에게 인증권한을 제거했어요".format(user_name), "인증이 해체되었습니다", "이제 {}님은 인증회원이 아니네요..".format(user_name)]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))
        no = discord.Embed(
            title="인증 해체",
            description="<@{}>님이 <@{}>님의 인증을 해체하였습니다!".format(str(ctx.author.id), str(user_name.id)),
            colour=0xB772CB
        )
        user = app.get_user(int(user_name.id))
        await user.send(embed=no)

@인증해체.error
async def 인증해체_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emoji = ["앗! 깜박하셨나요? 누구인지 않쓰셨어요", "누굴 줘야할지...", "저기요 뭐가 잘못된것같아요.. 누굴줘야할지 모르겠어요..", "대상을 선택안하셨는데..?"]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))
    if isinstance(error, commands.BadArgument):
        emoji = ["없는 유저라고 뜨는데.. 다시 확인해보세요!", "서버에 없으신것같은데.."]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))
    if isinstance(error, commands.MissingRole):
        emoji = ["당신은 권한이 없어요!", "당신은 나노네트워크 팀원이 아니신것같아요!", "팀원역활이 없으신것으로 확인했습니다!"]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))

@commands.has_role("인증 도움이 관리자권한")
@app.command(name="알림", pass_context=True)
async def 알림(ctx):
    channel = ctx.channel
    embed = discord.Embed(
        title="{}님의 알림설정창이에요!".format(ctx.author.name),
        description="알림을 활성화시 ⭕ 눌러주세요 비활성화시 ❌을 눌러주세요",
        colour=0xB772CB
    )
    embed2 = discord.Embed(
        title="{}님의 알림설정창이에요!".format(ctx.author.name),
        description="알림을 활성화로 설정되었어요!",
        colour=0xB772CB
    )
    embed3 = discord.Embed(
        title="{}님의 알림설정창이에요!".format(ctx.author.name),
        description="알림을 비활성화로 설정되었어요!",
        colour=0xB772CB
    )
    txte = await channel.send(embed=embed)
    await txte.add_reaction("⭕")
    await txte.add_reaction("❌")
    while True:
        try:
            reaction, user = await app.wait_for('reaction_add')  # Gets the reaction and the user with a timeout of 30 seconds + new Syntax
            if user == ctx.author:  # Test if the user is the author
                emoji = str(reaction.emoji)
                if emoji == '⭕':
                    await txte.clear_reactions()
                    await txte.edit(embed=embed2)
                    author = ctx.guild.get_member(int(ctx.author.id))
                    role = discord.utils.get(ctx.guild.roles, name="인증 알림(이름교체 하지마시요)")
                    await author.add_roles(role)
                    break
                elif emoji == '❌':
                    await txte.clear_reactions()
                    await txte.edit(embed=embed3)
                    author = ctx.guild.get_member(int(ctx.author.id))
                    role = discord.utils.get(ctx.guild.roles, name="인증 알림(이름교체 하지마시요)")
                    await author.remove_roles(role)
                    break
            if app.user != user:  # Test if it isn't the bot
                await txte.remove_reaction(reaction, user)
        except asyncio.TimeoutError:  # Handles Timeout
            break
    await txte.clear_reactions()


@알림.error
async def 알림_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        emoji = ["권한이 없습니다", "인증 도움이관리자가 있어야합니다."]
        randomNum = random.randrange(0, len(emoji))
        await ctx.send(str(emoji[randomNum]))

@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.content.startswith("/도움말"):
        channel = message.channel
        embed = discord.Embed(
            description="봇 명령어",
            colour = 0xB772CB
        )
        embed.add_field(name="인증유저가 되어봅시다!", value="`/인증 [마인크래프트 닉네임]`", inline=False)
        embed.add_field(name="인증해채 샷", value="`/인증해체 [마인크래프트 닉네임]`", inline=False)
        embed.add_field(name="인증, 문의 알림 설정을 해요!", value="`/알림`", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("/인증") and not message.content.startswith("/인증신청") and not message.content.startswith("/인증해체"):
        name = message.content[4:]
        if not name:
            await message.channel.send("마인크래프트의 닉네임을 입력해주세요!")
        else:
            now = datetime.datetime.now()
            embed = discord.Embed(
                title="인증 신청서",
                description="이모지을 클릭해 수락 또는 거절해주세요!\n\n신청유저 : <@{}>\n유저의 아이디 : {}\n유저의 마크닉네임 : {}\n신청일자 : ".format(message.author.id,message.author.id, str(name)) + str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second),
                colour=0xB772CB
            )
            await message.channel.send(f"<@{message.author.id}>님! 인증신청이 완료되었습니다!")
            channel = app.get_channel(734677642598416464)
            await channel.send("||<@&734680405789114418>||")
            msg = await channel.send(embed=embed)
            await msg.add_reaction("⭕")
            await msg.add_reaction("❌")
            while True:
                try:
                    reaction, user = await app.wait_for('reaction_add')  # Gets the reaction and the user with a timeout of 30 seconds + new Syntax
                    if int(user.bot) == False:
                        emoji = str(reaction.emoji)
                        if emoji == '⭕':
                            author = message.guild.get_member(int(message.author.id))
                            role = discord.utils.get(message.guild.roles, name="[✅] 인증유저")
                            await author.add_roles(role)
                            await message.author.edit(nick=str(name))
                            ok = discord.Embed(
                                title="인증유저 수락",
                                description=f"<@{str(user.id)}>님이 <@{message.author.id}>님의 인증신청을 수락하였습니다!",
                                colour=0xB772CB
                            )
                            await msg.clear_reactions()
                            await msg.edit(embed=ok)
                            user = app.get_user(int(message.author.id))
                            await user.send(embed=ok)
                            break
                        elif emoji == '❌':
                            no = discord.Embed(
                                title="인증유저 거절",
                                description=f"<@{str(user.id)}>님이 <@{message.author.id}>님의 인증신청을 거절하였습니다",
                                colour=0xB772CB
                            )
                            await msg.clear_reactions()
                            await msg.edit(embed=no)
                            user = app.get_user(int(message.author.id))
                            await user.send(embed=no)
                            break
                except asyncio.TimeoutError:  # Handles Timeout
                    break
                    
access_token = os.environ["BOT_TOKEN"]
app.run(access_token)
