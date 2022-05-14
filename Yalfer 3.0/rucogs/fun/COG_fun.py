from statistics import variance
from tkinter import Variable
import error_send
import discord
import random
import sqlite3
import datetime
from config import config
from discord.ext import commands
from rucogs.fun.system import FunCogFunctionality
#<<------------->>
class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
    
    def get_prefix(self, cursor, message):
        cursor.execute(
            "SELECT * FROM prefixes WHERE guild_id = ?", 
            (
                message.guild.id,
            )
        )
        result = cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return "+"
#<<респект----->>
    @commands.command(aliases = ['Респект', 'респект'])
    async def respect(self, ctx, member: discord.Member):
        if member == ctx.author:
            emb = discord.Embed(title = '💛 Нет, нет, нет!', description="Респектнуть самому себе нельзя!", colour=config.EMBED_COLOR_WHAT)
            await ctx.reply(embed=emb, mention_author=False)
        else:
            self.connection.commit()
            hearts = ["💖", "💛", "💚", "💙", "💜"]
            emb = discord.Embed(color=config.EMBED_COLOR, title = '😻 Уважение:', description = f"{ctx.author.mention} респектнул {member.mention} {random.choice(hearts)}\
            \n\n> **Рейтинг** {member.mention}: `+1`")
            date = datetime.datetime.today()
            emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
            await ctx.reply(embed=emb, mention_author=False)

#<<дуэль------->>
    @commands.command(aliases = ['Дуэль', 'дуэль', 'Дуель', 'дуель'])
    async def duel(self, ctx, member: discord.Member):
        if member == ctx.author:
            emb = discord.Embed(title = '💛 Нет, нет, нет!',description="Сражаться самим c собой не получится!", colour=config.EMBED_COLOR_WHAT)
            return await ctx.reply(embed=emb, mention_author=False)
        if member:
                variable = [
                f'> {member.mention} потерпел поражение\
                \n> {ctx.author.mention} остался в живых!',
                
                f'> {ctx.author.mention} был застрелен...\
                \n> {member.mention} остался в живых!',

                f'> {member.mention} убежал с поля боя!',

                f'> У {member.mention} осечка!\
                \n> {ctx.author.mention} остался в живых!',

                f'> У {ctx.author.mention} осечка!\
                \n> {member.mention} остался в живых!']     
                emb = discord.Embed(color=config.EMBED_COLOR, title='💥 Итоги поединка:', description = '{}'.format(random.choice(variable)))
                date = datetime.datetime.today()
                emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
                await ctx.reply(embed = emb, mention_author=False)

#<<краш--------->>
    @commands.command(aliases=['Краш', 'краш'])
    async def love(self, ctx, *, member: discord.Member):
        member = member or ctx.author
        r = random.randint(1, 100)
        k = random.randint(1, 5)
        hot = r / k

        if hot > 70:
            emoji_love = "💞"
        elif hot > 50:
            emoji_love = "💖"
        elif hot > 25:
            emoji_love = "💝"
        else:
            emoji_love = "💔"
        

        emb = discord.Embed(color=config.EMBED_COLOR, title=f'💕 Симпатия:', description = f'{member.mention} краш на `{hot:.2f}`% {emoji_love}!')
        emb.set_footer(icon_url = member.avatar_url, text = f'{member}')
        await ctx.reply(embed=emb, mention_author=False)

#<<судьба------->>
    @commands.command(aliases = ['Судьба', 'судьба'])
    async def ball(self, ctx, *, text):
        variable = ['Даааа! :innocent:', 
        'Ага щас :face_with_monocle: ', '100%', 
        'Нет и ещё раз нет! :no_entry_sign: ', 
        'Ты что?\nНЕТ! :four_leaf_clover: ', 
        'Не хочу тебя огорчать... :eyes: ', 
        'Хо-хо-хо. YES :heart_eyes:', 
        'Скорее нет, чем да :wave:', 
        'Маловероятно :moyai: ', 
        'Может быть :gem: ', 
        'Так и будет :heart_on_fire: ', 
        'А зачем это тебе?  :eggplant: ']
        await ctx.reply('{}'.format(random.choice(variable)), mention_author=False)

#<<монетка------>>
    @commands.command(aliases=['Орёл', 'орёл', 'Орел', 'орел'])
    async def orel(self, ctx):
        win = ["💖", "🤩", "😜", "👻", "💎"]
        lose = ["😳", "💀", "🤐", "👀", "🤨"]
        gameplay = ['{} Ты угадал. Это `орёл`!'.format(random.choice(win)), 
        '{} Ты смог! Именно `орёл` находится на выпавшей стороне!'.format(random.choice(win)), 
        '{} На выпавшей стороне виднеется `орёл`!'.format(random.choice(win)), 
        '{} Ты угадал... Это `орёл`!'.format(random.choice(win)), 
        '{} Да! Да! Да!'.format(random.choice(win)),

        '{} Нет. Это `решка`!'.format(random.choice(lose)), 
        '{} Ха-ха-ха! `Решка` находится на выпавшей стороне!'.format(random.choice(lose)), 
        '{} На выпавшей стороне виднеется `решка`!'.format(random.choice(lose)), 
        '{} Луууузер... Это `решка`!'.format(random.choice(lose)), 
        '{} Нет! Нет! Нет!'.format(random.choice(lose))]

        await ctx.reply('{}'.format(random.choice(gameplay)), mention_author=False)

    @commands.command(aliases=['Решка', 'решка'])
    async def reshka(self, ctx):
        win = ["💖", "🤩", "😜", "👻", "💎"]
        lose = ["😳", "💀", "🤐", "👀", "🤨"]
        gameplay = ['{} Ты угадал. Это `решка`!'.format(random.choice(win)), 
        '{} Ты смог! Именно `решка` находится на выпавшей стороне!'.format(random.choice(win)), 
        '{} На выпавшей стороне виднеется `решка`!'.format(random.choice(win)), 
        '{} Ты угадал... Это `решка`!'.format(random.choice(win)), 
        '{} Да! Да! Да!'.format(random.choice(win)),

        '{} Нет. Это `орёл`!'.format(random.choice(lose)), 
        '{} Ха-ха-ха! `Орёл` находится на выпавшей стороне!'.format(random.choice(lose)), 
        '{} На выпавшей стороне виднеется `орёл`!'.format(random.choice(lose)), 
        '{} Луууузер... Это `орёл`!'.format(random.choice(lose)), 
        '{} Нет! Нет! Нет!'.format(random.choice(lose))]
        
        await ctx.reply('{}'.format(random.choice(gameplay)), mention_author=False)
#<<------------->>
def setup(bot):
   bot.add_cog(Fun(bot))            