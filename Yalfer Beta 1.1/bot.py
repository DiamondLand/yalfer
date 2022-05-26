import discord
from discord.ext import commands
import random
import datetime
from discord.utils import get

client = commands.Bot(command_prefix = '.')

bad_words = ['уебан','пидр','мать в канаве','самоубийство','слит', 'гондон', 'гандон', 'пизда', 'хуй встал', 'пидорас', 'пидарас', 'порно', 'хуйня']


#Запуск-------------------------------------------------
@client.event

async def on_ready():
   print( 'BOT CONNECTED!')
   
   guilds = await client.fetch_guilds(limit = None).flatten()
   await client.change_presence(status = discord.Status.idle, activity = discord.Activity(name=f'за {len(guilds)} серверами', type= discord.ActivityType.watching))


@client.event
async def on_command_error(ctx, error):
    pass

#Фильтрация---------------------------------------------
@client.event

async def on_message(message):
   await client.process_commands(message)
   msg = message.content.lower() #Во всех регистрах
   if msg in bad_words:
    await message.delete()
    await message.author.send('**Не надо такое писать :rolling_eyes: **') 

#хелп-------------------------------------------------
@client.command(pass_context = True)

async def хелп(ctx): 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'КОМАНДЫ:')
   emb.add_field(name = '.прости @Участник', value = '```Попроси прощения```' )
   emb.add_field(name = '.обним @Участник', value = '```Обнимашки!```' )
   emb.add_field(name = '.кулачёк @Участник', value = '```Дружеский кулачёк```' )
   emb.add_field(name = '.грусть', value = '```Погрусти```' )
   emb.add_field(name = '.загадка', value = '```Загадка от бота```')
   emb.add_field(name = '.время', value = '```Узнай дату и время```' )

   emb.add_field(name = '.утро', value = '```Доброе утро от бота```' )
   emb.add_field(name = '.ночь', value = '```Спокойной ночи от бота```' )
   emb.add_field(name = '.фильм', value = '```Список интересных фильмов```')
   emb.add_field(name = '.орёл / .решка', value = '```Популярная игра "Орёл или Решка"```')


   emb.add_field(name = '.админком', value = '```Список команд для админов```' )
   emb.add_field(name = '.бот', value = '```Вся информация о боте```')

   emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
   await ctx.send(embed = emb)

#бот----------------------------------------------------
@client.command(pass_context = True)

async def бот(ctx): 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), title = '**Я хоть и и злостный снаружи, но добрый внутри**')
   emb.add_field(name = '**Имя бота:**', value = '```Yalfer```')
   emb.add_field(name = '**Версия:**', value = '```BETA 1.0```')
   emb.add_field(name = '**Префикс:**', value = '```.```')
   emb.add_field(name = '**Функционал бота:**', value = '```.хелп```')
   emb.add_field(name = '**Дата начала работы:**', value = '```21.03.2021```')
   emb.add_field(name = '**Создатель:**', value = '```Diamond#3533```')
   emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
   await ctx.send(embed = emb)

#фильм----------------------------------------------------
@client.command(pass_context = True)
async def фильм(ctx): 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Топ лучших комедий от меня:')
   emb.add_field(name = 'Брюс Всемогущий (2003)', value = ' ```Пессимист Брюс Нолан — популярный ведущий теленовостей. Его ничего не интересует: ни девушка Грейс, ни собственные репортажи. Но однажды Брюса увольняют. Разочарованный герой бросает вызов Богу и неожиданно получает ответ Всевышнего. Бог предлагает Брюсу поменяться с ним местами на неделю и посмотреть, сможет ли Брюс сделать мир хоть чуточку лучше.```')
   emb.add_field(name = 'На море!(2008)', value = '```Две семьи с друзьями решают провести новогодние каникулы большой и шумной компанией на Канарских островах. Пока в России холодная зима, они будут наслаждаться солнцем и морем. Казалось бы, нашему туристу ничто не может помешать. Однако обстоятельства не позволят им не то что искупаться, а даже одним глазком увидеть море.```')
   emb.add_field(name = 'Няньки (1994)', value = '```Владельцу транспортной компании угрожают, намекая на двух племянников — близнецов, оставшихся без родителей и живущих у него. И тогда он нанимает двух бесшабашных братьев-качков в качестве телохранителей. Малолетние племяннички дают прикурить нянькам, изобретая все новые и новые каверзы. Но Питера и Дэвида голыми руками не возьмешь: в конце концов, они находят общий язык с маленькими разбойниками```')
   emb.add_field(name = 'Мистер Бин', value = '```Мистер Бин - личность выдающаяся по количеству глупейших ситуаций, в которых он оказывается, и по оригинальности методов, с помощью которых он из этих ситуаций выкручивается. Идет ли он в библиотеку, сдает ли экзамены, собирается ли пообедать или прыгнуть с вышки в бассейне, заезжает ли он на автостоянку или раздевается на пляже, - редко кто сделает это так смешно и остроумно, как мистер Бин.```')
   emb.add_field(name = 'Познакомьтесь с Уолли Спарксом (1997)', value = '```Ведущие развлекательных телепрограмм Америки стараются всеми способами перещеголять друг друга. У любимца публики – Уолли Спаркса нет проблем: он доводит шутками людей до истерики. Но однажды заходит слишком далеко, «пройдясь» по губернатору. Шоу оказывается под угрозой. И Уолли бросается в бой – он не тот человек, которого можно остановить!```')
   emb.add_field(name = 'Снова в школу (1986)', value = '```57-летний миллионер Торнтон Мелон, владелец сети магазинов «Большой и толстый» в результате неожиданного визита к сыну выясняет, что письма Джейсона из колледжа о том, что он входит в число самых одаренных студентов, успешно выступает в команде прыгунов в воду и занимает мысли всех девушек, на самом деле всего лишь выдумка. Но Торнтон так этого не оставит! Он едет к сыну и начинает учиться с ним вместе```')
   await ctx.author.send(embed = emb)

   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention}, подборка фильмов отправлена тебе **личные сообщения!**')
   await ctx.send(embed = emb)

#админком--------------------------------------------------
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def админком(ctx): 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), title = 'КОМАНДЫ ДЛЯ АДМИНИСТРАЦИИ:')
   emb.add_field(name = '.очист', value = '```Удаление 10.000 сообщений```' )
   emb.add_field(name = '.очист (число)', value = '```Удаление заданного (числа) сообщений```' )
   emb.add_field(name = '.кик @участник', value = '```Кик @участника с сервера!```' )
   emb.add_field(name = '.бан @участник', value = '```Бан @участника на сервере!```' )
   emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
   await ctx.author.send(embed = emb)

   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention}, список команд отправлен тебе **личные сообщения!**')
   await ctx.send(embed = emb)

@админком.error
async def admincom_error(ctx, error):
   if isinstance (error, commands.MissingPermissions): 
    author = ctx.message.author
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете использовать `.админком`, так как у вас **отсутствуют права администратора!**')
    await ctx.send(embed = emb)


#личка--------------------------------------------------
@client.command()
async def личка(ctx, member: discord.Member):
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), description = f'{member.mention}, тебе анономно передали привет!')
   await member.send(embed = emb)
   
#орёл или решка----------------------------------------
@client.command(pass_context=True)
async def орёл(ctx):
   variable = ['Выпала решка. Проигрыш!','Выпал орёл. Победа!','Выпала решка. Проигрыш!']
   emb = discord.Embed(colour = discord.Color.dark_orange(), title = "{}".format(random.choice(variable)))
   await ctx.send(embed = emb)

@client.command(pass_context=True)
async def решка(ctx):
   variable = ['Выпал орёл. Проигрыш!','Выпала решка Победа!','Выпал орёл. Проигрыш!']
   emb = discord.Embed(colour = discord.Color.dark_orange(), title = "{}".format(random.choice(variable)))
   await ctx.send(embed = emb)

#загадка-----------------------------------------------
@client.command(pass_context = True)

async def загадка(ctx): 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), title = '**ЗАГАДКА:**' ' ')
   emb.add_field(name = 'Уровень сложности: Средний', value = '```Без ног и без рук, а художник еще тот```' )
   emb.set_footer(text = 'Пример ответа: .бот')
   await ctx.send(embed = emb)


@client.command(pass_context = True)

async def мороз(ctx): 
   author = ctx.message.author 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.blurple(), description = f'**{author.mention}, поздравляю! Ты дал верный ответ!**')
   await ctx.send(embed = emb)

#обним----------------------------------------------------
@client.command(pass_context = True)

async def обним(ctx, member: discord.Member ): #команда .обнять @Участника
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'{author.mention} обнимает {member.mention}!')
   emb.set_image(url = 'https://i.ytimg.com/vi/tBkrWiajhIg/maxresdefault.jpg') #Картинка в тексте
   await ctx.send( embed = emb)

@обним.error 
async def love_error(ctx, error):

  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите @Участника')
   await ctx.send(embed = emb)

#кулачёк----------------------------------------------------
@client.command(pass_context = True)

async def кулачёк(ctx, member: discord.Member ): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'{author.mention} и {member.mention} ')
   emb.set_image(url = 'https://demotivation.ru/wp-content/uploads/2020/06/157516.jpg') 
   await ctx.send( embed = emb)

@кулачёк.error 
async def hand_error(ctx, error):

  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите @Участника')
   await ctx.send(embed = emb)

#грусть----------------------------------------------------
@client.command(pass_context = True)

async def грусть(ctx): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'{author.mention} грустит')
   emb.set_image(url = 'http://2.bp.blogspot.com/-5OEnjJJX-vg/T_foYepsDiI/AAAAAAAAFBg/HqvpeVxfvIY/s1600/The+Lonesome+Mouse+(6).jpg') 
   await ctx.send(embed = emb)

@грусть.error 
async def sad_error(ctx, error):

  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите @Участника')
   await ctx.send(embed = emb)

#прости----------------------------------------------------
@client.command(pass_context = True)

async def прости(ctx, member: discord.Member ): 
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'{member.mention}, прости пожалуйста {author.mention}')
   emb.set_image(url = 'https://i.ytimg.com/vi/_yfrwQn2DH4/maxresdefault.jpg') 
   await ctx.send( embed = emb)

@прости.error 
async def sorry_error(ctx, error):

  if isinstance(error,commands.MissingRequiredArgument):
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**ОШИБКА!** {author.mention}, введите @Участника')
   await ctx.send(embed = emb)

#утро---------------------------------------------------
@client.command(pass_context = True)

async def утро(ctx): 
   author = ctx.message.author 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'**Утро – всегда страдания... Согласен, {author.mention}?**')
   await ctx.send(embed = emb)

#ночь---------------------------------------------------
@client.command(pass_context = True)

async def ночь(ctx): #команда .ночь
   author = ctx.message.author 
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.dark_orange(), description = f'**Желаю тебе самых приятных снов, дорогой {author.mention}**')
   await ctx.send(embed = emb)

#время---------------------------------------------------
@client.command(pass_context = True)

async def время(ctx):
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(title = '**ДАТА И ВРЕМЯ**', colour = discord.Color.dark_orange()) 
   emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url) #Упоминание автора сообщения и его аватарки в футере
   emb.set_thumbnail(url = 'https://cdn0.iconfinder.com/data/icons/flat-designed-circle-icon-2/1000/clock.png') #Cсылка на картинку с верху
   now_date = datetime.datetime.now()
   emb.add_field(name = 'Time', value = 'Time : {}'.format(now_date))
   await ctx.send(embed = emb)

#очистка чата-------------------------------------------
@client.command(pass_context = True)
@commands.has_permissions(administrator = True) #Только админы могут использовать эту команду

async def очист(ctx, amount = 10000): #.очистить очищает 10 000 сообщений
   await ctx.channel.purge(limit = 1)
   await ctx.channel.purge(limit = amount) #.очистить (число) очищает заданное кол-во сообщений
   author = ctx.message.author
   emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention} произвёл очистку чата на **{amount}** сообщений!')
   await ctx.send(embed = emb)

@очист.error
async def clear_error(ctx, error):

  if isinstance(error,commands.MissingPermissions): #Участнику без роли АДМИН будет писаться ошибка
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете очищать чаты, так как у вас **отсутствуют права администратора!**')
   await ctx.send(embed = emb)
   
#кик----------------------------------------------------
@client.command(pass_context = True)
@commands.has_permissions(administrator = True) #Только админы могут использовать эту команду

async def кик(ctx, member: discord.Member, *, reason = None): #Кик метод
    await ctx.channel.purge(limit = 1)
    await member.kick(reason = reason)
    emb = discord.Embed(colour = discord.Color.red(), description = f'**КИК!** {member.mention} был кикнут администратором') #Сообщение при кике
    emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = emb)

@кик.error
async def kick_error(ctx, error):

  if isinstance(error,commands.MissingPermissions): #Участнику без роли АДМИН будет писаться ошибка
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете кикать участников, так как у вас **отсутствуют права администратора!**')
   await ctx.send(embed = emb)

#бан----------------------------------------------------
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def бан(ctx, member: discord.Member, *, reason = None): #Бан метод
   await ctx.channel.purge(limit = 1)
   await member.ban(reason = reason)
   emb = discord.Embed(colour = discord.Color.red(), description = f'**БАН!** {member.mention} был забанен администратором') #Сообщение при бане
   emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
   await ctx.send(embed = emb)

@бан.error 
async def ban_error(ctx, error):

  if isinstance(error,commands.MissingPermissions): #Участнику без роли АДМИН будет писаться ошибка
   author = ctx.message.author
   await ctx.channel.purge(limit = 1)
   emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы не можете банить участников, так как у вас **отсутствуют права администратора!**')
   await ctx.send(embed = emb)

#Запуск-------------------------------------------------

token = open ('token.txt', 'r').readline()

client.run(token)

