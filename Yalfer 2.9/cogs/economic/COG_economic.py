from ast import alias
import sqlite3
import asyncio
import os
import sys
import random
import time
from discord.ext.commands.core import command
from loguru import logger
import discord
from discord.ext import commands
from discord.utils import get
from cogs.economic.system import EconomicCogFunctionality
from config import config

class EconomyCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
    
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

    #баланс-------------------------------------------------
    @commands.command(aliases = ['Баланс', 'баланс', 'Бал', 'бал'])
    async def bal(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        """
        :param ctx:
        :return:
        """
        data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            user,
            ctx.guild
        )
        await EconomicCogFunctionality.send_balance_info(ctx, user, data)

    #банк-------------------------------------------------
    @commands.command(aliases = ['Вбанк', 'вбанк'])
    async def to_bank(self, ctx, balance: int):
        
        """
        :param ctx:
        :param balance:
        :return:
        """
        member = ctx.message.author
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member, 
            ctx.guild
        )
        if user_data[3] < int(balance):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'У Вас отсутствует данная сумма!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if user_data[2] >= 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    - balance,
                    user_data
                )
                EconomicCogFunctionality.change_bank_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    balance,
                    user_data
                )
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Аккаунт {member}:', description = f'💖 Перевёл в банк `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #избанка-------------------------------------------------
    @commands.command(aliases = ['Избанка', 'избанка'])
    async def from_bank(self, ctx, balance: int):
        """
        :param ctx:
        :param balance:
        :return:
        """
        member = ctx.message.author
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member, 
            ctx.guild
        )
        if user_data[2] < int(balance):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'У Вас отсутствует данная сумма!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            users_balance = int(
                user_data[3]
            )
            if int(balance) + users_balance > 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    balance,
                    user_data
                )
                EconomicCogFunctionality.change_bank_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    - balance,
                    user_data
                )
                self.conn.commit()
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Аккаунт {member}:', description = f'💖 Обналичил `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #кража-------------------------------------------------
    @commands.command(aliases = ['Украсть', 'украсть', 'Кража', 'кража'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def grab(self, ctx, member: discord.Member):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        balance = random.randint(5000, 50000)
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if user_data[2] >= 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if users_balance < 50000:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'У {member.mention} недостаточно средств!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                grab = random.randint(1, 3)
                if grab == 1:
                    EconomicCogFunctionality.change_balance(
                        self.cursor,
                        self.conn,
                        member,
                        ctx.guild,
                        -balance,
                        user_data
                    )
                    user_data = EconomicCogFunctionality.get_user_data(
                        self.cursor,
                        self.conn,
                        ctx.author,
                        ctx.guild
                    )
                    EconomicCogFunctionality.change_balance(
                        self.cursor,
                        self.conn,
                        ctx.author,
                        ctx.guild,
                        balance,
                        user_data
                    )
                    emb = discord.Embed(color = config.EMBED_COLOR, title=f'Аккаунт {ctx.author}:', description = f'💖 Обокрал {member.mention} на `{balance}`💸!')
                    await ctx.reply(embed = emb, mention_author=False)
                else:
                    emb = discord.Embed(color = config.EMBED_COLOR, title=f'Аккаунт {ctx.author}:', description = f'💔 Пытался обокрасть {member.mention}, но не смог!')
                    await ctx.reply(embed = emb, mention_author=False)

    #установитьбанк-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Устбанк', 'устбанк'])
    async def set_wallet_bank(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        if int(balance) < 0:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if int(balance) > 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                server = ctx.guild
                self.cursor.execute(
                    "UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
                    (
                        balance,
                        member.id,
                        server.id
                    )
                )
                self.conn.commit()
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Банк {member}:', description = f'💖 Установлен на `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #добавитьбанк-------------------------------------------------	
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Добанк', 'добанк', 'Доббанк' ,'доббанк'])
    async def add_bal_bank(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member, 
            ctx.guild
        )
        if int(balance) <= 0:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if int(balance) + user_data[2] > 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                user_data = EconomicCogFunctionality.get_user_data(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild
                )
                EconomicCogFunctionality.change_bank_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    balance,
                    user_data
                )
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Банк {member}:', description = f'💖 Добавлено `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #установить-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Установить', 'установить'])
    async def set_wallet(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        if int(balance) > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if int(balance) < 0:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                server = ctx.guild
                self.cursor.execute(
                    "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                    (
                        balance,
                        member.id,
                        server.id
                    )
                )
                self.conn.commit()
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Установлен на `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #добавить-------------------------------------------------	
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Добавить', 'добавить'])
    async def add_bal(self, ctx, member: discord.Member, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if int(balance) <= 0:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                user_data = EconomicCogFunctionality.get_user_data(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild
                )
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    balance,
                    user_data
                )
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Добавлено `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)
      
    #бонус---------------------------------------------------------------------
    @commands.command(aliases = ['Бонус', 'бонус'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def bonus(self, ctx, balance = 5000):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. У тебя и так много денег!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Получено `{balance}`💸!')
            await ctx.reply(embed = emb, mention_author=False)

    #доктор------------------------------------------------------------
    @commands.command(aliases = ['Доктор', 'доктор'])
    @commands.cooldown(1, 10800, commands.BucketType.member)
    async def doctor(self, ctx, balance = config.MEDIC):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. У тебя и так много денег!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Получено `{balance}`💸!')
            await ctx.reply(embed = emb, mention_author=False)


    #пилот------------------------------------------------------------
    @commands.command(aliases = ['Пилот', 'пилот'])
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def pilot(self, ctx, balance = config.PILOT):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. У тебя и так много денег!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Получено `{balance}`💸!')
            await ctx.reply(embed = emb, mention_author=False)

    #учитель--------------------------------------------------------
    @commands.command(aliases = ['Шахтёр', 'шахтёр', 'Шахтер', 'шахтер'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def worker(self, ctx, balance = config.WORKER):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. У тебя и так много денег!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Получено `{balance}`💸!')
            await ctx.reply(embed = emb, mention_author=False)

    #передать-------------------------------------------------------------------
    @commands.command(aliases = ['Передать', 'передать'])
    async def send_gift(self, ctx, member: discord.Member, cash: int):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(cash) + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. Давай не так много, окей?')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            """
            :param ctx:
            :param member:
            :param cash:
            :return:
            """
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            getter_balance = int(
                EconomicCogFunctionality.get_user_data(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild
                )[3]
            )
            users_balance = int(
                user_data[3]
            )
            if int(cash) <= 0:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                if int(cash) > users_balance:
                    emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'У Вас недостаточно средств!')
                    await ctx.reply(embed = emb, mention_author=False)
                else:
                    self.cursor.execute(
                        "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                        (
                            users_balance - int(cash),
                            ctx.message.author.id,
                            ctx.guild.id
                        )
                    )
                    self.cursor.execute(
                        "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                        (
                            getter_balance + int(cash),
                            member.id,
                            ctx.guild.id
                        )
                    )
                    self.conn.commit()
                    emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {member}:', description = f'💖 Получено `{cash}`💸!')
                    await ctx.reply(embed = emb, mention_author=False)

    #казино-------------------------------------------------
    @commands.command(aliases=["Казино", "казино", 'Ставка', 'ставка'])
    @commands.cooldown(2, 13, commands.BucketType.member)
    async def slot(self, ctx, balance: int):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance)*3 + users_balance > 999999999999999999:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Брат, брат, брат. У тебя и так много денег!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if int(balance) <= 0:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                member = ctx.message.author
                getter_balance = int(
                EconomicCogFunctionality.get_user_data(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild
                )[3]
                )			
                user_data = EconomicCogFunctionality.get_user_data(
                    self.cursor,
                    self.conn,
                    ctx.message.author,
                    ctx.guild
                )
                users_balance = int(
                    user_data[3]
                )
                if int(balance) > users_balance:
                    emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'У Вас недостаточно средств!')
                    await ctx.reply(embed = emb, mention_author=False)
                else:			
                    emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
                    a = random.choice(emojis)
                    b = random.choice(emojis)
                    c = random.choice(emojis)

                    slotmachine = f"**{a} {b} {c}**"

                    if (a == b == c):
                        user_data = EconomicCogFunctionality.get_user_data(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild
                        )
                        member = ctx.message.author
                        EconomicCogFunctionality.change_balance(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild,
                            balance *3,
                            user_data
                        )
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\nВыручка: `{balance*4}` ✨")
                        emb.set_footer(text = f'3/3 совпадения!')
                        await ctx.reply(embed = emb, mention_author=False)
                    elif (a == b) or (a == c) or (b == c):
                        user_data = EconomicCogFunctionality.get_user_data(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild
                        )
                        member = ctx.message.author
                        EconomicCogFunctionality.change_balance(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild,
                            balance *2,
                            user_data
                        )
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\nВыручка: `{balance*3}` 🎉")
                        emb.set_footer(text = f'2/3 совпадения!')
                        await ctx.reply(embed = emb, mention_author=False)
                    else:
                        user_data = EconomicCogFunctionality.get_user_data(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild
                        )

                        EconomicCogFunctionality.change_balance(
                            self.cursor,
                            self.conn,
                            ctx.message.author,
                            ctx.guild,
                            - balance,
                            user_data
                        )
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\nВы проиграли! 😶")
                        emb.set_footer(text = f'0/3 совпадения!')
                        await ctx.reply(embed = emb, mention_author=False)

    #пожертвовать-------------------------------------------------
    @commands.command(aliases = ['Пожертовать', 'пожертвовать'])
    async def fond(self, ctx, balance: int):
        """
        :param ctx:
        :param balance:
        :return:
        """
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        if int(balance) <= 0:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            if user_data[3] < int(balance):
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'У Вас недостаточно средств!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    ctx.message.author,
                    ctx.guild,
                    - balance,
                    user_data
                )
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Баланс {ctx.author}:', description = f'💖 Пожертвовал `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

    #вмагаз-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['вмагазин', 'Вмагазин', 'Вмагаз', 'вмагаз'])
    async def add_shop_item(self, ctx, role: discord.Role, prise: int):
        """
        :param ctx:
        :param role:
        :param prise:
        :return:
        """
        if int(prise) <= 0:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Сумма ввода должна быть больше чем `0`!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            self.cursor.execute(
                "INSERT INTO economic_shop_item VALUES(?, ?, ?)",
                (
                    ctx.guild.id,
                    role.id,
                    prise
                )
            )
            self.conn.commit()
            emb = discord.Embed(color = config.EMBED_COLOR, title=f'Пополнение магазина!', description = f'💖 {role.mention} - `{prise}`💸!')
            await ctx.reply(embed = emb, mention_author=False)

    #измагаза-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Измагазина', 'измагазина', 'измагаза', 'Измагаза'])
    async def del_shop_item(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        self.cursor.execute(
            "DELETE FROM economic_shop_item WHERE guild_id = ? AND role_id = ?",
            (
                ctx.guild.id,
                role.id,
            )
        )
        self.conn.commit()
        emb = discord.Embed(color = config.EMBED_COLOR, title=f'Изъятие из магазина!', description = f'💔 {role.mention}')
        await ctx.reply(embed = emb, mention_author=False)

    #магаз-------------------------------------------------
    @commands.command(aliases = ['Магазин', 'магазин', 'Магаз', 'магаз'])
    async def shop(self, ctx):
        prefix = self.get_prefix(self.cursor, ctx.message)
        """
        :param ctx:
        :return:
        """
        data = EconomicCogFunctionality.get_all_shop_items(
            self.cursor,
            ctx.guild
        )
        data.reverse()
        emb = discord.Embed(color = config.EMBED_COLOR, title="Магазин ролей:")
        for item in data:
            emb.add_field(name='Роль:', value=f"{ctx.guild.get_role(item[1]).mention} - `{item[2]}`", inline=False)
            emb.set_footer(text = f'❓ Купить {prefix}купить @роль')
        await ctx.send(embed = emb)

    #купить------------------------------------------------
    @commands.command(aliases = ['Купить', 'купить'])
    async def buy(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        data = EconomicCogFunctionality.get_all_shop_items(
            self.cursor,
            ctx.guild
        )
        role_exists = False
        balance = 0
        for item in data:
            if item[1] == role.id:
                role_exists = True
                balance = item[2]
                break
        member = ctx.message.author
        if not role_exists:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'Данной роли нет в магазине!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(self.cursor, self.conn, ctx.message.author, ctx.guild)
            if user_data[3] < int(balance):
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'У Вас недостаточно средств!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    member,
                    ctx.guild,
                    - balance,
                    user_data
                )
                await ctx.message.author.add_roles(role)
                emb = discord.Embed(color = config.EMBED_COLOR, title=f'Аккаунт {ctx.author}:', description = f'💖 Купил {role.mention} за `{balance}`💸!')
                await ctx.reply(embed = emb, mention_author=False)

def setup(client):
    """
    :param client:
    :return:
    """
    client.add_cog(EconomyCog(client))

