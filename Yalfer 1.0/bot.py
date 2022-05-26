import discord
import random
import datetime
import requests
import io
import re
import urllib.parse
import urllib.request
import os
import youtube_dl
import asyncio
import json

from discord.utils import get
from pymongo import MongoClient
from discord.utils import find
from urllib.parse import urljoin
from discord.ext import commands
from random import randint
from discord.ext.commands import Bot
from asyncio import TimeoutError
from collections.abc import Sequence


bot = commands.Bot(command_prefix = '.', help_command = None)

queue = []
bad_words = ['уебан', 'пидр', 'мать в канаве', 'самоубийство', 'слиты боты', 'слит', 'гондон', 'гандон', 'пизда', 'хуйло', 'хуй', 'пидорас', 'пидарас', 'порно', 'хуйня', 'снюс', 'наркотики', 'наркота', 'вейп']

#Запуск-------------------------------------------------
@bot.event
async def on_ready():
   print('BOT CONNECTED!')
   guilds = await bot.fetch_guilds(limit = None).flatten()
   await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name = f'за {len(guilds)} серверами', type = discord.ActivityType.watching))

@bot.command(aliases = ['Серверлист', 'серверлист'])
async def guilds(ctx):
    emb = discord.Embed(colour = discord.Color.blurple(), title = 'Yalfer используется на:', description = "\n".join(map(str, bot.guilds)))
    await ctx.send(embed = emb)

#личка--------------------------------------------------
@bot.command(aliases = ['Личка'])
async def личка(ctx, member: discord.Member, *, text):
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.gold(), description = f'{author.mention} передал тебе: **{text}**')
   await member.send(embed = emb)

   emb = discord.Embed(colour = discord.Color.green(), description = f':white_check_mark: {author.mention}, `личное сообщение` доставлено!')
   await ctx.send(embed = emb)

@личка.error 
async def is_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника` и `текст для передачи`')
   await ctx.send(embed = emb)

#выстрел-----------------------------------------------
@bot.command(aliases = ['Выстрел'])
async def выстрел(ctx):
   variable = ['Пусто! :tada: ', 'Пусто! :tada: ', 'Пусто! :tada: ', 'Пусто! :tada: ', 'Осечка!  :tada: :tada: :tada: ', '`Пуля`! Вы были убиты... :gun: ']
   emb = discord.Embed(colour = discord.Color.gold(), description = '{}'.format(random.choice(variable)))
   await ctx.send(embed = emb)

#судьба------------------------------------------------
@bot.command(aliases = ['Судьба'])
async def судьба(ctx, *, text):
   variable = ['Конечно! :comet: ', 'Ты что? **НЕТ**! :no_entry_sign: ', 'Возможно... :four_leaf_clover: ', 'Ни за что! :o: ', 'Естественно! :sparkles: ', 'Да, да, да! :ringed_planet: ']
   emb = discord.Embed(colour = discord.Color.gold(), description = '{}'.format(random.choice(variable)))
   await ctx.send(embed = emb)

@судьба.error 
async def sudba_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `ваш вопрос` к судьбе')
   await ctx.send(embed = emb)

#орёл или решка----------------------------------------
@bot.command(aliases = ['Орёл', 'орел', 'Орел'])
async def орёл(ctx):
   variable = ['Выпала `решка`. **Проигрыш**! :stuck_out_tongue: ', 'Выпал `орёл`. **Победа**! :tada: ']
   emb = discord.Embed(colour = discord.Color.gold(), description = '{}'.format(random.choice(variable)))
   await ctx.send(embed = emb)

@bot.command(aliases = ['Решка'])
async def решка(ctx):
   variable = ['Выпал `орёл`. **Проигрыш**! :stuck_out_tongue: ', 'Выпала `решка`. **Победа**! :tada: ']
   emb = discord.Embed(colour = discord.Color.gold(), description = "{}".format(random.choice(variable)))
   await ctx.send(embed = emb)

#шутка----------------------------------------------
@bot.command(aliases = ['Шутка', 'Щутка', 'щутка'])
async def шутка(ctx):
   variable = ['— Что ты делаешь?\n— Ищу счастье.\n— В холодильнике?\n— Ну, где-то же оно должно быть...',
   'Спорят две бабки:\n- Ты дура!\n- Сама, ты дура!\nПодходит дед:\n- Да не спорьте! Вы обе правы!',
   'Из школьного сочинения:\nТатьяна написала Онегину письмо с признанием в любви, но тот сразу же отправил его в спам!',
   '- Машенька, какие фрукты ты любишь больше всего?\n- Мороженное!',
   'Мои внуки учатся онлайн.\nПрошу администрацию школы сдать деньги на новые шторы и ремонт мебели',
   'Встречаются две подруги:\n- Дорогая, ты так поправилась!\n-Это я ещё похудела! Ты меня месяц назад не видела. Была, как ты сейчас!',
   'Сегодня у меня музыкальное отношение к жизни...\nМне все по барабану!',
   'Молодая женщина качает у подъезда коляску с грудным ребёнком. Мимо проходит её знакомая и, внимательно глядя на младенца, говорит:\n- Ну, надо же! Как две капли воды похож на твоего мужа! Женщина задумчиво:\n - Вообще-то это соседка с третьего этажа попросила меня немного побыть с её ребёнком...',
   'Детство - это когда ты не паришься из-за чьего-то мнения.\nТебе просто плевать, обсыпал урода песком и всё',
   'Ненавижу март, потому что он всегда ставит передо мной слишком сложный выбор:\nЗажариться в зимней куртке или замерзнуть в весеннем пальто',
   'А есть новые матерные слова? А то старые уже не справляются с ситуацией',
   'Сантехник был приятно удивлен, когда засунул руку в унитаз и пожал её там кому-то другому',
   'Сколько вам нужно времени? — Сделаю за час в течение недели',
   'Ваша фамилия?\n— Пук.\nКак?\n— Не Как, а Пук',
   'Программист пришел на стрельбище. Дали ему автомат, он отстрелял весь рожок, не попал даже в мишень. Инструктор начинает его ругать, на что программист внимательно осматривает свой автомат и говорит:\nУ меня все пули вылетели, проблемы на вашей стороне',
   'Доктор, а вы уверены, что во время вакцинации необходимо быть без лифчика?',
   'Спартанским воинам говорили:\n«Вернись с щитом!».\nИмея в виду: «Не просрите щит!»',
   'Ты грубый.\n— Обоснуй, тварь',
   'Довольно иронично, что интернет был создан для экономии времени',
   '«Мы почти и пришли!», — сказал Сусанин, срывая на ходу банан…',]
   emb = discord.Embed(colour = discord.Color.gold(), description = '{}'.format(random.choice(variable)))
   await ctx.send(embed = emb)

#загадки-----------------------------------------------
@bot.command(aliases = ['Загадки'])
async def загадки(ctx): 
   emb = discord.Embed(colour = discord.Color.gold(), title = 'ЗАГАДКИ ПО УРОВНЮ СЛОЖНОСТИ:')
   emb.add_field(name = 'Лёгкий:', value = '`.загадка`' )
   emb.add_field(name = 'Средний:', value = '`.ззагадка`')
   emb.add_field(name = 'Сложный:', value = '`.зззагадка`')
   emb.set_footer(text = 'Загадки изменяются каждое обновление!')
   await ctx.send(embed = emb)

#загадка-------------------------------------------------
@bot.command(aliases = ['Загадка'])
async def загадка(ctx): 
   emb = discord.Embed(colour = discord.Color.gold(), title = 'ЛЁГКАЯ ЗАГАДКА:')
   emb.add_field(name = '**Загадка:**', value = '```Вспушит она свои бока,\nСвои четыре уголка,\nИ тебя, как ночь настанет,\nВсё равно к себе притянет```' )
   emb.add_field(name = '**Ответ:**', value = '`.ответ`', inline = False)
   await ctx.send(embed = emb)

@bot.command(aliases = ['Подушка'])
async def подушка(ctx):
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description = f'{author.mention}, ты разгадал `лёгкую загадку`! Усложним? `.ззагадка`')
   await ctx.send(embed = emb)

#ззагадка-------------------------------------------------
@bot.command(aliases = ['Ззагадка'])
async def ззагадка(ctx): 
   emb = discord.Embed(colour = discord.Color.gold(), title = 'СРЕДНЯЯ ЗАГАДКА:')
   emb.add_field(name = '**Загадка:**', value = '```И сияет, и блестит, никому оно не льстит```' )
   emb.add_field(name = '**Ответ:**', value = '`.ответ`', inline = False)
   await ctx.send(embed = emb)

@bot.command(aliases = ['Зеркало'])
async def зеркало(ctx): 
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description = f'{author.mention}, ты разгадал `среднюю загадку`! Усложним? `.зззагадка`')
   await ctx.send(embed = emb)

#загадка3-------------------------------------------------
@bot.command(aliases = ['Зззагадка'])
async def зззагадка(ctx): 
   emb = discord.Embed(colour = discord.Color.gold(), title = 'СЛОЖНАЯ ЗАГАДКА:')
   emb.add_field(name = '**Загадка:**', value = '```Стоит дуб,\nВ нем двенадцать гнезд,\nВ каждом гнезде по четыре яйца,\nВ каждом яйце по семи цыпленков?```' )
   emb.add_field(name = '**Ответ:**', value = '`.ответ`', inline = False)
   await ctx.send(embed = emb)

@bot.command(aliases = ['Год'])
async def год(ctx): 
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description = f'{author.mention}, ты разгадал `сложную загадку`!')
   await ctx.send(embed = emb)

#утро---------------------------------------------------
@bot.command(aliases = ['Утро'])
async def утро(ctx): 
   author = ctx.message.author 
   emb = discord.Embed(colour = discord.Color.gold(), description = f'Утро – всегда страдашки... Правда, {author.mention}? :blueberries:')
   await ctx.send(embed = emb)

#ночь---------------------------------------------------
@bot.command(aliases = ['Ночь'])
async def ночь(ctx): 
   author = ctx.message.author 
   emb = discord.Embed(colour = discord.Color.gold(), description = f'Желаю таких же слаких снов, как синнабона, дорогой {author.mention} :tea: ')
   await ctx.send(embed = emb)

#ютуб----------------------------------------------------
@bot.command(aliases = ['Ютуб'])
async def ютуб(msg, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    emb = discord.Embed(colour = discord.Color.gold(), title = 'Нажмите для просмотра в YouTube', url = 'http://www.youtube.com/watch?v=' + search_results[0])
    emb.set_footer(text = 'Создатель не несёт ответственность за ваши поисковые запросы!')
    await msg.send(embed = emb)

@ютуб.error
async def youtube_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `название видео`')
   await ctx.send(embed = emb)

#яндекс-------------------------------------------------
@bot.command(aliases = ['Яндекс'])
async def яндекс(ctx, *, text):
    emb = discord.Embed(colour = discord.Color.gold(), title = 'Нажмите для просмотра в Yandex', url = f'https://www.yandex.ru/search/?lr=213&offline_search=1&text={text}')
    emb.set_footer(text = 'Создатель не несёт ответственность за ваши поисковые запросы!')
    await ctx.send(embed = emb)

@яндекс.error
async def yandex_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `название запроса` без пробелов!')
   await ctx.send(embed = emb)

#юзер-------------------------------------------------
@bot.command(aliases = ['Юзер'])
async def юзер(ctx, member :discord.Member, guild: discord.Guild = None):
   emb = discord.Embed(title = 'ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:', colour = discord.Color.blurple())
   emb.add_field(name = 'Имя:', value = member.display_name, inline = False)
   emb.add_field(name = "ID:", value = member.id, inline = False)
   emb.add_field(name = 'Наивысшая роль на сервере:', value = f'{member.top_role.mention}', inline = False)
   emb.add_field(name = 'Акаунт был создан:', value = member.created_at.strftime('%#d %B %Y, %I:%M %p'), inline = False)
   emb.set_thumbnail(url = member.avatar_url)
   await ctx.send(embed = emb)

@юзер.error 
async def user_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника`')
   await ctx.send(embed = emb)

#очистка чата-------------------------------------------
@bot.command(aliases = ['Очист'])
@commands.has_permissions(administrator = True)
async def очист(ctx, amount = 10000):
   await ctx.channel.purge(limit = 1)
   await ctx.channel.purge(limit = amount)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention} произвёл очистку чата на **{amount}** сообщений!')
   await ctx.send(embed = emb)

@очист.error
async def clear_error(ctx, error):
 if isinstance(error,commands.MissingPermissions): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете `очищать чаты`, так как у вас **отсутствуют права администратора!**')
   await ctx.send(embed = emb)

#кик----------------------------------------------------
@bot.command(aliases = ['Кик'])
@commands.has_permissions(administrator = True)
async def кик(ctx, member: discord.Member, *, reason): 
    await ctx.channel.purge(limit = 1)
    await member.kick(reason = reason)
    emb = discord.Embed(colour = discord.Color.red(), description = f'**КИК!** {member.mention} был `кикнут`\nКик выдал: {ctx.author.display_name}\nПричина: {reason}')
    await ctx.send(embed = emb)

@кик.error
async def kick_error(ctx, error):
 if isinstance(error,commands.MissingPermissions): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете `кикать участников`, так как у вас **отсутствуют права администратора!**')
   await ctx.send(embed = emb)

 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника` и причину кика')
   await ctx.send(embed = emb)

#бан----------------------------------------------------
@bot.command(aliases = ['Бан'])
@commands.has_permissions(administrator = True)
async def бан(ctx, member: discord.Member, *, reason): 
   await ctx.channel.purge(limit = 1)
   await member.ban(reason = reason)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**БАН!** {member.mention} был `забанен`\n Бан выдал: {ctx.author.display_name}\nПричина: {reason}')
   await ctx.send(embed = emb)

@бан.error 
async def ban_error(ctx, error):
 if isinstance(error,commands.MissingPermissions): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете `банить участников`, так как у вас **отсутствуют права администратора!**')                             #ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
   await ctx.send(embed = emb)

 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника` и причину бана')
   await ctx.send(embed = emb)

#фильм----------------------------------------------------
@bot.command(aliases = ['Фильм', 'Фильмы', 'фильмы'])
async def фильм(ctx): 
   author = ctx.message.author
   emb = discord.Embed(title = 'ПОДБОРКА КОМЕДИЙ:', colour = discord.Color.gold())
   emb.add_field(name = 'Брюс Всемогущий (2003)', value = 'Пессимист Брюс Нолан — популярный ведущий теленовостей. Его ничего не интересует: ни девушка Грейс, ни собственные репортажи. Но однажды Брюса увольняют. Разочарованный герой бросает вызов Богу и неожиданно получает ответ Всевышнего. Бог предлагает Брюсу поменяться с ним местами на неделю и посмотреть, сможет ли Брюс сделать мир хоть чуточку лучше', inline = False)
   emb.add_field(name = 'На море!(2008)', value = 'Две семьи с друзьями решают провести новогодние каникулы большой и шумной компанией на Канарских островах. Пока в России холодная зима, они будут наслаждаться солнцем и морем. Казалось бы, нашему туристу ничто не может помешать. Однако обстоятельства не позволят им не то что искупаться, а даже одним глазком увидеть море', inline = False)
   emb.add_field(name = 'Няньки (1994)', value = 'Владельцу транспортной компании угрожают, намекая на двух племянников — близнецов, оставшихся без родителей и живущих у него. И тогда он нанимает двух бесшабашных братьев-качков в качестве телохранителей. Малолетние племяннички дают прикурить нянькам, изобретая все новые и новые каверзы. Но Питера и Дэвида голыми руками не возьмешь: в конце концов, они находят общий язык с маленькими разбойниками', inline = False)
   emb.add_field(name = 'Мистер Бин "Катастрофа" (1997)', value = 'Мистер Бин работает смотрителем в Королевской Британской Галерее. Начальство давно уволило бы его по формулировке «за сон на рабочем месте», если бы не покровительство директора. Вместо этого Бина отправляют в командировку в Лос-Анджелес. Там его принимают за официальное лицо, приехавшее на открытие величайшей выставки США', inline = False)
   emb.add_field(name = 'Познакомьтесь с Уолли Спарксом (1997)', value = 'Ведущие развлекательных телепрограмм Америки стараются всеми способами перещеголять друг друга. У любимца публики – Уолли Спаркса нет проблем: он доводит шутками людей до истерики. Но однажды заходит слишком далеко, «пройдясь» по губернатору. Шоу оказывается под угрозой. И Уолли бросается в бой – он не тот человек, которого можно остановить!')
   emb.add_field(name = 'Снова в школу (1986)', value = '57-летний миллионер Торнтон Мелон, владелец сети магазинов «Большой и толстый» в результате неожиданного визита к сыну выясняет, что письма Джейсона из колледжа о том, что он входит в число самых одаренных студентов, успешно выступает в команде прыгунов в воду и занимает мысли всех девушек, на самом деле всего лишь выдумка. Но Торнтон так этого не оставит! Он едет к сыну и начинает учиться с ним вместе', inline = False)
   await author.send(embed = emb)
   emb = discord.Embed(colour = discord.Color.green(), description = f':white_check_mark: {author.mention}, `подборка фильмов` отправлена тебе в **личные сообщения!**')
   await ctx.send(embed = emb)

#хелп-------------------------------------------------
@bot.command(aliases = ['Хелп'])
async def хелп(ctx): 
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'СПИСОК КОМАНД:')
   emb.add_field(name = '---', value = '```Интересное:```', inline = False)
   emb.add_field(name = '⁣⁣Пожелания', value = '`.утро` **/** `.ночь`', inline = False)
   emb.add_field(name = '⁣⁣Загадки', value = '`.загадки`', inline = False)
   emb.add_field(name = '⁣⁣Случайная шутка', value = '`.шутка`', inline = False)
   emb.add_field(name = '⁣⁣Подборка комедий', value = '`.фильм`', inline = False)
   emb.add_field(name = '⁣⁣Поиск в Yandex', value = '`.яндекс [запрос без пробелов]`', inline = False)
   emb.add_field(name = '⁣⁣Поиск на YouTube', value = '`.ютуб [запрос]`', inline = False)
   emb.add_field(name = '⁣⁣Патреон', value = '`.патреон`', inline = False)
   emb.add_field(name = '⁣⁣Добавить бота', value = '`.добавить`', inline = False)
   emb.add_field(name = '⁣Инфо бота и ссылки', value = '`.бот`', inline = False)

   emb.add_field(name = '---', value = '```С упоминанием @Участника:```', inline = False)
   emb.add_field(name = '⁣⁣Передай сообщение в ЛС', value = '`.личка @Участник [сообщение для передачи]`', inline = False)
   emb.add_field(name = '⁣⁣Инфо участика', value = '`.юзер @Участник`', inline = False) 
   
   emb.add_field(name = '---', value = '```Игры:```', inline = False)
   emb.add_field(name = '⁣⁣Игра "Орёл или Решка"', value = '`.орёл` **/** `.решка`', inline = False)
   emb.add_field(name = '⁣⁣Игра "Русская рулетка"', value = '`.выстрел`', inline = False)
   emb.add_field(name = '⁣⁣Игра "Шар судьбы"', value = '`.судьба [ваш вопрос]`', inline = False)

   emb.add_field(name = '---', value = '```Для администрации:```', inline = False)
   emb.add_field(name = '⁣⁣Очистка чата на 10000 сообщений', value = '`.очист`', inline = False)
   emb.add_field(name = '⁣⁣Очистка чата на [число] сообщений', value = '`.очист [число]`', inline = False)
   emb.add_field(name = 'Кик', value = '`.кик @участник`', inline = False)
   emb.add_field(name = 'Бан⁣', value = '`.бан @участник`', inline = False)
   
   emb.set_footer(text = 'Всего команд: 17')


   await ctx.send(embed = emb)

#бот----------------------------------------------------
@bot.command(aliases = ['Бот'])
async def бот(ctx): 
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'ИНФОРМАЦИЯ О БОТЕ:')
   emb.add_field(name = 'Имя бота:', value = '`Yalfer`')
   emb.add_field(name = 'Версия:', value = '`1.0`')
   emb.add_field(name = 'Префикс:', value = '`.`')
   emb.add_field(name = 'Функционал бота:', value = '`.хелп`')
   emb.add_field(name = 'Дата начала работы:', value = '`21.03.2021`')
   emb.add_field(name = 'Создатель:', value = '`Simofor#3533`')

   emb.add_field(name = 'Поддержка:', value = '`.дс`')
   emb.add_field(name = 'Добавить бота:', value = '`.добавить`')
   emb.add_field(name = 'Патреон:', value = '`.патреон`')
   await ctx.send(embed = emb)

#патреон-------------------------------------------------
@bot.command(aliases = ['Патреон', 'донат', 'Донат'])
async def патреон(ctx):
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Patreon', url = 'https://www.patreon.com/simoforyalferdiscordbot' )
   emb.add_field(name = '`Поддержка на Patreon`', value = 'Для тех, кто хочет `поддержать` мои старания', inline = False)
   await ctx.send(embed = emb)

#добавить-----------------------------------------------
@bot.command(aliases = ['Добавить'])
async def добавить(ctx):
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Добавить', url = 'https://discord.com/api/oauth2/authorize?client_id=829311432335032321&permissions=2084564343&scope=bot')
   emb.add_field(name = '`Добавить бота`', value = 'Для тех, кто хочет `добавить бота` на свой сервер', inline = False)
   await ctx.send(embed = emb)

#дс------------------------------------------------------
@bot.command(aliases = ['Дс'])
async def дс(ctx):
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Сервер', url = 'https://discord.gg/ZJzBU8BZ/swdHNG7Jye')
   emb.add_field(name = '`Дискорд сервер`', value = 'Для тех, кто хочет `зайти на сервер поддержки`', inline = False)
   await ctx.send(embed = emb)

#экономика---------------------------------------------
@bot.command(aliases = ['Коины'])
async def коины(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(ctx.author.id) in money:
        money[str(ctx.author.id)] = {}
        money[str(ctx.author.id)]['Money'] = 0

    if not str(ctx.author.id) in queue:
        emb = discord.Embed(colour = discord.Color.green(), description=f'**{ctx.author}** Вы получили свои `1250` монет')
        await ctx.send(embed= emb)
        money[str(ctx.author.id)]['Money'] += 1250
        queue.append(str(ctx.author.id))
        with open('economy.json','w') as f:
            json.dump(money,f)
        await asyncio.sleep(12*60)
        queue.remove(str(ctx.author.id))
    if str(ctx.author.id) in queue:
        emb = discord.Embed(description=f'**{ctx.author}** Вы `уже получили` свою награду!')
        await ctx.send(embed= emb)

@bot.command(aliases = ['Баланс'])
async def баланс(ctx,member:discord.Member = None):
    if member == ctx.author or member == None:
        with open('economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(colour = discord.Color.gold(),description=f'У **{ctx.author}** {money[str(ctx.author.id)]["Money"]} монет')
        await ctx.send(embed= emb)
    else:
        with open('economy.json','r') as f:
            money = json.load(f)
        emb = discord.Embed(colour = discord.Color.gold(),description=f'У **{member}** {money[str(member.id)]["Money"]} монет')
        await ctx.send(embed= emb)

@bot.command(aliases = ['Мдобавить'])
@commands.has_permissions(administrator = True)
async def мдобавить(ctx,role:discord.Role,cost:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        await ctx.send("Эта роль уже есть в магазине")
    if not str(role.id) in money['shop']:
        money['shop'][str(role.id)] ={}
        money['shop'][str(role.id)]['Cost'] = cost
        await ctx.send('Роль добавлена в магазин')
    with open('economy.json','w') as f:
        json.dump(money,f)

@мдобавить.error 
async def add_error(ctx, error):
 if isinstance(error,commands.MissingPermissions): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете `управлять магазином`, так как у вас **отсутствуют права администратора!**')                       
   await ctx.send(embed = emb)

@bot.command(aliases = ['Магазин'])
async def магазин(ctx):
    with open('economy.json','r') as f:
        money = json.load(f)
    emb = discord.Embed(colour = discord.Color.blurple(), title="Магазин")
    for role in money['shop']:
        emb.add_field(name=f'Цена: {money["shop"][role]["Cost"]}',value=f'<@&{role}>',inline=False)
    await ctx.send(embed=emb)

@bot.command(aliases = ['Мубрать'])
@commands.has_permissions(administrator = True)
async def мубрать(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if not str(role.id) in money['shop']:
        await ctx.send("Этой роли нет в магазине")
    if str(role.id) in money['shop']:
        await ctx.send('Роль удалена из магазина')
        del money['shop'][str(role.id)]
    with open('economy.json','w') as f:
        json.dump(money,f)

@мубрать.error 
async def remove_error(ctx, error):
 if isinstance(error,commands.MissingPermissions): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете `управлять магазином`, так как у вас **отсутствуют права администратора!**')                       
   await ctx.send(embed = emb)

@bot.command(aliases = ['Купить'])
async def купить(ctx,role:discord.Role):
    with open('economy.json','r') as f:
        money = json.load(f)
    if str(role.id) in money['shop']:
        if money['shop'][str(role.id)]['Cost'] <= money[str(ctx.author.id)]['Money']:
            if not role in ctx.author.roles:
                await ctx.send('Вы купили роль!')
                for i in money['shop']:
                    if i == str(role.id):
                        buy = discord.utils.get(ctx.guild.roles,id = int(i))
                        await ctx.author.add_roles(buy)
                        money[str(ctx.author.id)]['Money'] -= money['shop'][str(role.id)]['Cost']
            else:
                await ctx.send('У вас уже есть эта роль!')
    with open('economy.json','w') as f:
        json.dump(money,f)

@bot.command(aliases = ['Подарить'])
async def подарить(ctx,member:discord.Member,arg:int):
    with open('economy.json','r') as f:
        money = json.load(f)
    if money[str(ctx.author.id)]['Money'] >= arg:
        emb = discord.Embed(description=f'**{ctx.author}** подарил **{member}** `{arg}` монет')
        money[str(ctx.author.id)]['Money'] -= arg
        money[str(member.id)]['Money'] += arg
        await ctx.send(embed = emb)
    else:
        await ctx.send('У вас недостаточно денег')
    with open('economy.json','w') as f:
        json.dump(money,f)

@подарить.error 
async def present_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника` и сумму подарка')
   await ctx.send(embed = emb)


#Запуск-------------------------------------------------

token = open ('token.txt', 'r').readline()

bot.run(token)

