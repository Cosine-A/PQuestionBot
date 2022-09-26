import discord
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

token = 'MTAyMzczNTk4NzM3MDczMzU4OQ.G5oUbF.OU63eeZ1rldXEb_MQ_QlcXPsaIGiX76A4BA8FI'

question_channel = 1023737546808770701
answer_channel = 1023747940243738644

now = datetime.now()


@bot.event
async def on_ready():
    state_message = discord.Game("모든 기능 테스트")
    await bot.change_presence(status=discord.Status.online, activity=state_message)


@bot.event
async def on_message(message):
    if message.channel.id != question_channel:
        return
    await message.delete()

    author = message.author
    content = message.content

    first_button = Button(label="답변 시작", style=discord.ButtonStyle.green, emoji="👆")

    async def first_callback(interaction):
        guild_id = interaction.message.guild.id
        message_id = interaction.message.id

        await interaction.message.delete()
        early_channel = await bot.get_guild(guild_id).create_text_channel(
            name=f"question-{message_id}",
            category=bot.get_channel(1023737563397242954))
        new_channel = bot.get_channel(early_channel.id)

        second_button = Button(label="답변 완료", style=discord.ButtonStyle.green, emoji="👆")

        async def second_callback(interaction2):
            limit = -1
            async for _ in new_channel.history(limit=None):
                limit += 1

            message_list = []
            async for messages in new_channel.history(limit=limit):
                message_list.append(messages.content)
            answer = list_to_message(message_list)

            if not answer:
                answer = "답변 내용이 없습니다."

            success_answer = create_answer_embed("답변이 도착하였습니다.", interaction2.user, content, answer)
            await bot.get_user(message.author.id).send(embed=success_answer)

            await new_channel.delete()

        second_button.callback = second_callback

        view2 = View()
        view2.add_item(second_button)

        second_embed = create_question_embed("해당 문의를 선택하였습니다.", author, content, 0xff0000)
        await new_channel.send(embed=second_embed, view=view2)

    first_button.callback = first_callback

    view = View()
    view.add_item(first_button)

    first_embed = create_question_embed("문의가 도착했습니다.", author, content, 0x008000)

    await bot.get_channel(answer_channel).send(embed=first_embed, view=view)


def list_to_message(message: list):
    reverse_list = message
    reverse_list.reverse()
    final_message = ""
    for messages in reverse_list:
        final_message += messages + "\n"
    return final_message


def create_question_embed(title, author, value, color):
    embed = discord.Embed(title=title, description=f"문의자: {author}", color=color)
    embed.add_field(name="문의 내용", value=value, inline=False)
    now_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}"
    embed.set_footer(text=f"질문 - {now_time}")
    return embed


def create_answer_embed(title, author, question, answer):
    embed = discord.Embed(title=title, description=f"답변자: {author}", color=0xffff00)
    embed.add_field(name="문의 내용", value=question, inline=False)
    embed.add_field(name="답변 내용", value=answer, inline=False)
    now_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}"
    embed.set_footer(text=f"답변 - {now_time}")
    return embed


bot.run(token)
