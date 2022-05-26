import discord
from discord.ext import commands
import random
import datetime
import requests
import io
import re
import urllib.parse
import urllib.request

from discord.utils import get
from discord.utils import get
from random import randint
from asyncio import TimeoutError

client = commands.Bot(command_prefix = '.')

bad_words = ['уебан', 'пидр', 'мать в канаве', 'самоубийство', 'слиты боты', 'слит', 'гондон', 'гандон', 'пизда', 'хуйло', 'хуй', 'пидорас', 'пидарас', 'порно', 'хуйня', 'снюс', 'наркотики', 'наркота', 'вейп']

#Запуск-------------------------------------------------
@client.event

async def on_ready():
   print( 'BOT CONNECTED!')
   #activity = discord.Game(name = 'Chatch it! || .хелп', type = 1)
   #await client.change_presence(status = discord.Status.online, activity = activity)

   guilds = await client.fetch_guilds(limit = None).flatten()
   await client.change_presence(status = discord.Status.idle, activity = discord.Activity(name=f'за {len(guilds)} серверами', type= discord.ActivityType.watching))

@client.event
async def on_command_error(ctx, error):
    pass

#Фильтрация---------------------------------------------
@client.event
async def on_message(message):
   await client.process_commands(message)
   msg = message.content.lower() 
   if msg in bad_words:
    await message.delete()
    emb = discord.Embed(colour = discord.Color.red(), description = '**Не надо** такое писать! :rolling_eyes:')
    await message.author.send(embed = emb)
#личка--------------------------------------------------
@client.command(aliases = ['Личка'])
async def личка(ctx, member: discord.Member, *, text):
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.blurple(), description = f'{author.mention} передал тебе: **{text}**')
   await member.send(embed = emb)
   emb = discord.Embed(colour = discord.Color.green(), description = ':white_check_mark: Сообщение **доставлено**!')
   await ctx.send(embed = emb)

@личка.error 
async def is_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника` и `текст для передачи`')
   await ctx.send(embed = emb)

#орёл или решка----------------------------------------
@client.command(aliases = ['Орёл', 'орел', 'Орел'])
async def орёл(ctx):
   variable = ['Выпала `решка`. Проигрыш!', 'Выпал `орёл`. Победа!']
   emb = discord.Embed(colour = discord.Color.gold(), title = '{}'.format(random.choice(variable)))
   await ctx.send(embed = emb)

@client.command(aliases = ['Решка'])
async def решка(ctx):
   variable = ['Выпал `орёл`. Проигрыш!', 'Выпала `решка`. Победа!']
   emb = discord.Embed(colour = discord.Color.gold(), title = "{}".format(random.choice(variable)))
   await ctx.send(embed = emb)

#загадка-----------------------------------------------
@client.command(aliases = ['Загадка'])
async def загадка(ctx): 
   emb = discord.Embed(colour = discord.Color.gold(), title = '**ЗАГАДКА:**' ' ')
   emb.add_field(name = 'Уровень сложности: Сложный', value = '```Один мужчина способен начисто сбрить бороду больше десяти раз в день, при этом продолжая ходить бородатым. Кто он?```' )
   emb.set_footer(text = 'Пример ответа: ".бот" / сдаться: ".сдаться"')
   await ctx.send(embed = emb)

@client.command(aliases = ['Брадобрей', 'бродобрей', 'Бродобрей', 'брадабрей', 'Брадабрей'])
async def брадобрей(ctx): 
   author = ctx.message.author 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.green(), description = f'{author.mention}, поздравляю! Ты **разгадал** загадку, дав **верный** ответ!')
   await ctx.send(embed = emb)

@client.command(aliases = ['Сдаться', 'сдатся', 'Сдатся'])
async def сдаться(ctx): 
   author = ctx.message.author 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, жаль, что ты **не смог разгадать** загадку. Ответ `.брадобрей`')
   await ctx.author.send(embed = emb)
   emb = discord.Embed(colour = discord.Color.green(), description = f':white_check_mark: {author.mention}, `Ответ на загадку` отправлен тебе в **личные сообщения**!')
   await ctx.send(embed = emb)


#обним----------------------------------------------------
@client.command(aliases = ['Обним'])
async def обним(ctx, member: discord.Member): 
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.gold(), description = f'{author.mention} обнимает {member.mention}!')
   await ctx.send(embed = emb)

@обним.error 
async def love_error(ctx, error):
  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника`')
   await ctx.send(embed = emb)

#прости----------------------------------------------------
@client.command(aliases = ['Прости'])
async def прости(ctx, member: discord.Member ): 
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.gold(), description = f'{member.mention}, прости пожалуйста {author.mention}')
   await ctx.send( embed = emb)

@прости.error 
async def sorry_error(ctx, error):
  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника`')
   await ctx.send(embed = emb)

#утро---------------------------------------------------
@client.command(aliases = ['Утро'])
async def утро(ctx): 
   author = ctx.message.author 
   emb = discord.Embed(colour = discord.Color.gold(), description = f'Утро – всегда страдашки... Правда, {author.mention}? :blueberries:')
   await ctx.send(embed = emb)

#ночь---------------------------------------------------
@client.command(aliases = ['Ночь', 'вечер', 'Вечер'])
async def ночь(ctx): 
   author = ctx.message.author 
   emb = discord.Embed(colour = discord.Color.gold(), description = f'Желаю таких же слаких снов, как синнабона, дорогой {author.mention} :tea: ')
   await ctx.send(embed = emb)
   
#дата---------------------------------------------------
@client.command(aliases = ['Дата'])
async def дата(ctx):
   emb = discord.Embed(colour = discord.Color.gold(), title = '**УЗНАЙ ДАТУ И ВРЕМЯ**') 
   emb.set_thumbnail(url = 'https://cdn0.iconfinder.com/data/icons/flat-designed-circle-icon-2/1000/clock.png') 
   now_date = datetime.datetime.now()
   emb.add_field(name = '---', value = '`Дата и время:` {}'.format(now_date))
   await ctx.send(embed = emb)

#добавить-----------------------------------------------
@client.command(aliases = ['Добавить'])
async def добавить(ctx):
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Добавить', url = 'https://discord.com/api/oauth2/authorize?client_id=829311432335032321&permissions=4228906103&scope=bot')
   emb.add_field(name = '**Предупреждение:**', value = '```Бот не находиться на хостинге и работает не круглосуточно. Это временно```' )
   await ctx.send(embed = emb)

#ютуб----------------------------------------------------
@client.command(aliases = ['Ютуб'])
async def ютуб(msg, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    emb = discord.Embed(colour = discord.Color.gold(), title = 'Нажмите для просмотра',url = 'http://www.youtube.com/watch?v=' + search_results[0])
    await msg.send(embed = emb)

@ютуб.error
async def youtube_error(ctx, error):
 if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `название видео`')
   await ctx.send(embed = emb)

#очистка чата-------------------------------------------
@client.command(aliases = ['Очист'])
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
@client.command(aliases = ['Кик'])
@commands.has_permissions(administrator = True)
async def кик(ctx, member: discord.Member, *, reason = None): 
    await ctx.channel.purge(limit = 1)
    author = ctx.message.author
    await member.kick(reason = reason)
    emb = discord.Embed(colour = discord.Color.red(), description = f'**КИК!** {member.mention} был ``кикнут`` администратором {author.mention}')
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
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника`')
   await ctx.send(embed = emb)

#бан----------------------------------------------------
@client.command(aliases = ['Бан'])
@commands.has_permissions(administrator = True)
async def бан(ctx, member: discord.Member, *, reason = None): 
   await ctx.channel.purge(limit = 1)
   author = ctx.message.author
   await member.ban(reason = reason)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**БАН!** {member.mention} был `забанен` администратором {author.mention}')
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
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите `@Участника`')
   await ctx.send(embed = emb)

#юзер-------------------------------------------------
@client.command(aliases = ['Юзер'])
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

#фильм----------------------------------------------------
@client.command(aliases = ['Фильм', 'Фильмы', 'фильмы'])
async def фильм(ctx): 
   embed1 = discord.Embed(colour = discord.Color.gold(), title = 'Фильмы воспроизводятся через сайт "LordFilms"', description = 'Сайт и бот не имеют связи между собой. Yalfer не использует сайт в целях получения денег. Если вы владелец этого сайта и считаете, что ваши авторские права нарушены, напишите в личные сообщения мне (Simofor#3533), приведя доказательства того, что вы владелец сайта.')
   embed2 = discord.Embed(colour = discord.Color.gold(), title = 'Брюс Всемогущий (2003)', url = 'http://ab-online.lordfilms-s.cc/44949-film-brjus-vsemoguschij-2003.html', description = 'Пессимист Брюс Нолан — популярный ведущий теленовостей. Его ничего не интересует: ни девушка Грейс, ни собственные репортажи. Но однажды Брюса увольняют. Разочарованный герой бросает вызов Богу и неожиданно получает ответ Всевышнего. Бог предлагает Брюсу поменяться с ним местами на неделю и посмотреть, сможет ли Брюс сделать мир хоть чуточку лучше')
   embed3 = discord.Embed(colour = discord.Color.gold(), title = 'На море!(2008)', url = 'https://hd.lordsfilm.to/9345-na-more.html', description = 'Две семьи с друзьями решают провести новогодние каникулы большой и шумной компанией на Канарских островах. Пока в России холодная зима, они будут наслаждаться солнцем и морем. Казалось бы, нашему туристу ничто не может помешать. Однако обстоятельства не позволят им не то что искупаться, а даже одним глазком увидеть море')
   embed4 = discord.Embed(colour = discord.Color.gold(), title = 'Няньки (1994)', url = 'https://hd.lordsfilm.to/14778-njanki.html', description = 'Владельцу транспортной компании угрожают, намекая на двух племянников — близнецов, оставшихся без родителей и живущих у него. И тогда он нанимает двух бесшабашных братьев-качков в качестве телохранителей. Малолетние племяннички дают прикурить нянькам, изобретая все новые и новые каверзы. Но Питера и Дэвида голыми руками не возьмешь: в конце концов, они находят общий язык с маленькими разбойниками')
   embed5 = discord.Embed(colour = discord.Color.gold(), title = 'Мистер Бин "Катастрофа" (1997)', url = 'http://ab-online.lordfilms-s.cc/27926-film-mister-bin-1997.html', description = 'Мистер Бин работает смотрителем в Королевской Британской Галерее. Начальство давно уволило бы его по формулировке «за сон на рабочем месте», если бы не покровительство директора. Вместо этого Бина отправляют в командировку в Лос-Анджелес. Там его принимают за официальное лицо, приехавшее на открытие величайшей выставки США')
   embed6 = discord.Embed(colour = discord.Color.gold(), title = 'Познакомьтесь с Уолли Спарксом (1997)', url = 'http://ab-online.lordfilms-s.cc/30059-film-poznakomtes-s-uolli-sparksom-1996.html', description = 'Ведущие развлекательных телепрограмм Америки стараются всеми способами перещеголять друг друга. У любимца публики – Уолли Спаркса нет проблем: он доводит шутками людей до истерики. Но однажды заходит слишком далеко, «пройдясь» по губернатору. Шоу оказывается под угрозой. И Уолли бросается в бой – он не тот человек, которого можно остановить!')
   embed7 = discord.Embed(colour = discord.Color.gold(), title = 'Снова в школу (1986)', url = 'http://ab-online.lordfilms-s.cc/33742-film-snova-v-shkolu-1986.html', description = '57-летний миллионер Торнтон Мелон, владелец сети магазинов «Большой и толстый» в результате неожиданного визита к сыну выясняет, что письма Джейсона из колледжа о том, что он входит в число самых одаренных студентов, успешно выступает в команде прыгунов в воду и занимает мысли всех девушек, на самом деле всего лишь выдумка. Но Торнтон так этого не оставит! Он едет к сыну и начинает учиться с ним вместе')

   embeds = [embed1, embed2, embed3, embed4, embed5, embed6, embed7]
   message = await ctx.send(embed = embed1)
   page = pag (client, message, use_more = False, timeout = 1000000000, embeds = embeds)
   await page.start()

#хелп-------------------------------------------------
@client.command(aliases = ['Хелп'])
async def хелп(ctx): 
   emb = discord.Embed(colour = discord.Color.blurple(), title = '**СПИСОК КОМАНД:**')
   emb.add_field(name = '---', value = '```Интересное:```', inline = False)
   emb.add_field(name = '⁣⁣Пожелания', value = '`.утро` **/** `.ночь`', inline = False)
   emb.add_field(name = '⁣⁣Загадка', value = '`.загадка`', inline = False)
   emb.add_field(name = '⁣⁣Фильмы', value = '`.фильм`', inline = False)
   emb.add_field(name = '⁣⁣Дата и время', value = '`.дата`', inline = False)
   emb.add_field(name = '⁣⁣Найди видео на YouTube', value = '`.ютуб [название видео]`', inline = False)
   emb.add_field(name = '⁣Патреон', value = '`.патреон`', inline = False)
   emb.add_field(name = '⁣⁣Добавить бота к себе на сервер', value = '`.добавить`', inline = False)
   emb.add_field(name = '⁣Инфо бота', value = '`.бот`', inline = False)

   emb.add_field(name = '---', value = '```С упоминанием @Участника:```', inline = False)
   emb.add_field(name = '⁣⁣Передай сообщение в ЛС', value = '`.личка @Участник [сообщение для передачи]`', inline = False)
   emb.add_field(name = '⁣⁣Прости', value = '`.прости @Участник`', inline = False)
   emb.add_field(name = '⁣⁣Обнимашки', value = '`.обним @Участник`', inline = False)
   emb.add_field(name = '⁣⁣Инфо участика', value = '`.юзер @Участник`', inline = False)
   
   emb.add_field(name = '---', value = '```Игры:```', inline = False)
   emb.add_field(name = '⁣⁣Игра "Орёл или Решка"', value = '`.орёл` **/** `.решка`', inline = False)

   emb.add_field(name = '---', value = '```Для администрации:```', inline = False)
   emb.add_field(name = '⁣⁣Очистка чата на 10000 сообщений', value = '`.очист`', inline = False)
   emb.add_field(name = '⁣⁣Очистка чата на [число] сообщений', value = '`.очист [число]`', inline = False)
   emb.add_field(name = 'Кик и бан⁣ ', value = '`.кик` **/** `.бан @участник`', inline = False)

   emb.set_footer(text = 'Всего команд: 17')

   await ctx.send(embed = emb)

#бот----------------------------------------------------
@client.command(aliases = ['Бот'])
async def бот(ctx): 
   emb = discord.Embed(colour = discord.Color.blurple(), title = '**ИНФОРМАЦИЯ О БОТЕ:**')
   emb.add_field(name = 'Имя бота:', value = '`Yalfer`')
   emb.add_field(name = 'Версия:', value = '`Alfa 1.3`')
   emb.add_field(name = 'Префикс:', value = '`.`')
   emb.add_field(name = 'Функционал бота:', value = '`.хелп`')
   emb.add_field(name = 'Дата начала работы:', value = '`21.03.2021`')
   emb.add_field(name = 'Создатель:', value = '`Simofor#3533`')

   emb.add_field(name = '⁣⁣ ', value = '**Полезные ссылки:**', inline = False)
   emb.add_field(name = 'Поддержать разработчика:', value = 'https://www.patreon.com/simoforyalferdiscordbot', inline = False)
   emb.add_field(name = 'Сервер разработчика:', value = 'https://discord.gg/swdHNG7Jye', inline = False)
   emb.add_field(name = 'Игра от Simofor:', value = 'https://www.kartridge.com/games/Simofor_Studio/catch-it', inline = False)
   emb.add_field(name = 'Добавить бота к себе:', value = 'https://discord.com/api/oauth2/authorize?client_id=829311432335032321&permissions=4228906231&scope=bot', inline = False)
   emb.set_footer(icon_url = ctx.author.avatar_url, text = '- аватарка запросившего команду участника')
   await ctx.send(embed = emb)

#донат--------------------------------------------------
@client.command()
@commands.has_permissions(administrator = True)
async def fdzx(ctx):
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Patreon', url = 'https://www.patreon.com/simoforyalferdiscordbot' )
   emb.add_field(name = '`Поддержка на Patreon`', value = 'Для тех, кто хочет **поддержать** мои старания', inline = False)
   emb.set_footer(icon_url = ctx.author.avatar_url, text = '- аватарка участника, запросившего команду')
   await ctx.send(embed = emb)

#правила------------------------------------------------
@client.command()
@commands.has_permissions(administrator = True)
async def dfsq(ctx):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = discord.Color.blurple(), title = '**ПРАВИЛА:**')
    emb.add_field(name = '⁣⁣1.', value = 'Призывать к суициду **запрещено**!', inline = False)
    emb.add_field(name = '⁣⁣2.', value = 'Оскорбления **запрещены**!', inline = False)
    emb.add_field(name = '⁣⁣4.', value = 'Реклама сторонних ресурсов, иных контентов в ЛС в виде спама **запрещена**!', inline = False)
    emb.add_field(name = '5.', value = 'Распространение личной информации **запрещено**!', inline = False)
    emb.add_field(name = '⁣⁣6.', value = 'Обман, мошенничество, шантаж, а также продажа чего либо или предложения «халявы» **запрещено**!', inline = False)
    emb.add_field(name = '⁣⁣7.', value = 'Рассылка материалов в виде: порнографии, «хентай», насилие, вредные привычки (алкоголь, наркотики) **запрещена**!', inline = False)
    emb.add_field(name = '⁣⁣8.', value = 'Распространение пропаганды, ненависти к национальному, половому, религиозному признаку **запрещены**!', inline = False)
    emb.add_field(name = '⁣9.', value = 'Попрошайничество **запрещено**!', inline = False)
    emb.add_field(name = '⁣10.', value = 'Выдавать себя за другого человека **запрещено**!', inline = False)
    await ctx.send(embed = emb)
   
#Запуск-------------------------------------------------

token = open ('token.txt', 'r').readline()

client.run(token)

