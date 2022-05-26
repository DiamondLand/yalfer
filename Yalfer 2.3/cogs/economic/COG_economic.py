from ast import alias
import sqlite3
import asyncio
import os
import sys
import random
import time
from tkinter import N
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
        await ctx.channel.purge(limit=1)
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
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'У вас `нет` такой суммы!')
            await ctx.send(embed = emb, delete_after = 30)
            return
        else:
            if user_data[2] >= 100000000:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит банковского счёта - `100.000.000`')
                emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓Лимит налички - 50.000.000")
                await ctx.send(embed = emb, delete_after = 30)
                return
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы пополнили банковский счёт на `{balance}`💸!')
                await ctx.send(embed=emb)

    #избанка-------------------------------------------------
    @commands.command(aliases = ['Избанка', 'избанка', 'Избанк', 'избанк'])
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
            ctx.guild)
        server = ctx.guild
        if user_data[2] < int(balance):
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'У вас `нет` такой суммы!')
            await ctx.send(embed = emb, delete_after = 30)
            return
        else:
            users_balance = int(
                user_data[3]
            )
            if int(balance) + users_balance > 50000000:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
                emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
                await ctx.send(embed = emb, delete_after=15)
                return
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы забрали `{balance}`💸 с банковского счёта!')
                await ctx.send(embed=emb)

    #кража-------------------------------------------------
    @commands.command(aliases = ['Украсть', 'украсть', 'Кража', 'кража'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def g(self, ctx, member: discord.Member):
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
        if users_balance < 50000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'Увы, у {member.mention} нет `50000`💸')
            await ctx.send(embed = emb, delete_after=20)
            return
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
                author = ctx.author
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{author.mention} обокрал {member.mention} на `{balance}`💸!')
                await ctx.send(embed=emb)
                return
            else:
                author = ctx.author
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{author.mention} пытался обокрасть {member.mention}, но  него не получилось!')
                await ctx.send(embed=emb)
                return

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
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
            await ctx.send(embed = emb, delete_after=20)
        else:
            if int(balance) > 100000000:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит банковского счёта - `100.000.000`')
                emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
                await ctx.send(embed = emb, delete_after = 30)
                return
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'Банк {member.mention} установлен на `{balance}`💰!')
                await ctx.send(embed=emb)

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
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
            await ctx.send(embed = emb, delete_after=20)
        else:
            if int(balance) + user_data[2] > 100000000:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит банковского счёта - `100.000.000`')
                emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
                await ctx.send(embed = emb, delete_after = 30)
                return
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention} получил `{balance}` на банковский счёт💰!')
                await ctx.send(embed=emb)

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
        if int(balance) > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            if int(balance) < 0:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
                await ctx.send(embed = emb, delete_after=20)
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'Баланс {member.mention} установлен на `{balance}`💸!')
                await ctx.send(embed=emb)
                return

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
        if int(balance) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            if int(balance) <= 0:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
                await ctx.send(embed = emb, delete_after=20)
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention} получил `{balance}`💸!')
                await ctx.send(embed=emb)
                return
      
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
        if int(balance) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            emb.set_footer(text=f"❓ Лимит банковского счёта - 100.000.000\n❓ Лимит налички - 50.000.000")
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            await ctx.channel.purge(limit=1)
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
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸!')
            await ctx.send(embed = emb)
            return

    #чит-код---------------------------------------------------------------------
    @commands.command()
    async def yalfersimofor20212022(self, ctx, balance = 100000000):
        await ctx.channel.purge(limit=1)
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

    #доктор------------------------------------------------------------------------	
    @commands.command(aliases = ['Доктор', 'доктор'])
    @commands.cooldown(1, 10800, commands.BucketType.member)
    async def doctor(self, ctx, balance = 50000):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            await ctx.channel.purge(limit=1)
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            member = ctx.message.author
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Работа доктором:', description = f'Вы приходите в операционную и ждёте пациенита...')
            emb.set_footer(text = 'Ожидайте, пациента уже везут')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Пациент прибыл!', description = f'Вы моете руки, надеваете перчатки и готовитесь к операции...')
            emb.set_footer(text = 'Ожидайте, идёт подготовка к операции')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Подготовка завершена!', description = f'Подача наркоза, пациент медлено засыпает...')
            emb.set_footer(text = 'Ожидайте, идёт операция')
            await member.send(embed = emb, delete_after=15)
            time.sleep(3)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Завершение!', description = f'Всё прошло успешно. Пациента увозят в палату...')
            await member.send(embed = emb, delete_after=15)
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу доктором!')
            emb.set_footer(text = 'Возобновить данную работу можно через 3 часа!')
            await ctx.send(embed = emb, delete_after = 15)
            return


    #пилот------------------------------------------------------------
    @commands.command(aliases = ['Пилот', 'пилот'])
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def pilot(self, ctx, balance = 25000):
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            member = ctx.message.author
            await ctx.channel.purge(limit=1)
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild
            )
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Работа пилотом:', description = f'Вы садитесь в самолёт и проводите ЧЕК перед взлётом...')
            emb.set_footer(text = 'Ожидайте, выполняется ЧЕК')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Сбоев нет!', description = f'Вы выруливаете на ВПП и ждёте добро на взлёт...')
            emb.set_footer(text = 'Ожидайте добро на взлёт')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Добро получено!', description = f'Вы взлетаете. Попутного ветра!')
            emb.set_footer(text = 'Ожидайте, полёт начался')
            await member.send(embed = emb, delete_after=15)
            time.sleep(3)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Посадка!', description = f'Рейс успешно завершён!')
            await member.send(embed = emb, delete_after = 15)

            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу пилотом!')
            emb.set_footer(text = 'Возобновить данную работу можно через 2 часа!')
            await ctx.send(embed = emb, delete_after = 15)
            return

    #учитель--------------------------------------------------------
    @commands.command(aliases = ['Учитель', 'учитель'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def teacher(self, ctx, balance = 10000):
        member = ctx.message.author
        await ctx.channel.purge(limit=1)
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            ctx.message.author,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if int(balance) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Работа учителем:', description = f'Вы заходите в кабинет директора на планёрку...')
            emb.set_footer(text = 'Ожидайте, идёт планёрка')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Планёрка проведена!', description = f'Вы идёте в кабинет и ждёте начало урока...')
            emb.set_footer(text = 'Ожидайте, урок скоро начнётся')
            await member.send(embed = emb, delete_after=15)
            time.sleep(2)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Звонок на урок!', description = f'Дети заходят в класс, начинаются уроки!')
            emb.set_footer(text = 'Ожидайте, урок начался')
            await member.send(embed = emb, delete_after=15)
            time.sleep(3)
            emb = discord.Embed(color = config.EMBED_COLOR, title = 'Звонок с урока!', description = f'Все уроки прошли, ваш рабочий день завершён!')
            await member.send(embed = emb, delete_after=15)

            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу учителем!')
            emb.set_footer(text = 'Возобновить данную работу можно через 1 час!')
            await ctx.send(embed = emb, delete_after=15)
            return

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
        if int(cash) + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Лимит налички - `50.000.000`')
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            await ctx.channel.purge(limit=1)

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
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
                await ctx.send(embed = emb, delete_after=30)
                return
            else:
                if int(cash) > users_balance:
                    await ctx.channel.purge(limit=1)
                    emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'У вас `нет` такой суммы!')
                    await ctx.send(embed = emb, delete_after = 30)
                    return
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
                    author = ctx.message.author
                    emb = discord.Embed(color = config.EMBED_COLOR, description = f'{author.mention}, вы передали {member.mention} `{cash}`💸!')
                    await ctx.send(embed = emb)
                    return

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
        if int(balance)*3 + users_balance > 50000000:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title = 'Опасение!', description = 'Лимит налички - `50.000.000`, ваша ставка будет превышать лимит при `3/3`!')
            await ctx.send(embed = emb, delete_after=15)
            return
        else:
            if int(balance) <= 0:
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Кредитов.net!')
                await ctx.send(embed = emb, delete_after=20)
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
                    await ctx.channel.purge(limit=1)
                    emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'У вас `нет` такой суммы!')
                    await ctx.send(embed = emb, delete_after=20)
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
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\n`3/3` совпадения!\nВыручка: `{balance*4}` :four_leaf_clover:")
                        await ctx.send(embed=emb)
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
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\n`2/3` совпадения!\nВыручка: `{balance*3}` 🎉")
                        await ctx.send(embed=emb)
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
                        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{slotmachine}\nНе сошлось, вы проиграли 😢")
                        await ctx.send(embed=emb)
                        return

    #пожертвовать-------------------------------------------------
    @commands.command(aliases = ['Пожертовать', 'пожертвовать'])
    async def fond(self, ctx, balance: int):
        await ctx.channel.purge(limit=1)
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
        server = ctx.guild
        if int(balance) <= 0:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
            await ctx.send(embed = emb, delete_after=20)
        else:
            if user_data[3] < int(balance):
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR, description = 'У вас `нет` такой суммы!')
                await ctx.send(embed = emb, delete_after=20)
            else:
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.conn,
                    ctx.message.author,
                    ctx.guild,
                    - balance,
                    user_data
                )
                author = ctx.message.author
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{author.mention}, спасибо за пожертвование `{balance}`💸!')
                await ctx.send(embed = emb)

    #вмагаз-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['вмагазин', 'Вмагазин', 'Вмагаз', 'вмагаз'])
    async def add_shop_item(self, ctx, role: discord.Role, prise: int):
        await ctx.channel.purge(limit=1)
        """
        :param ctx:
        :param role:
        :param prise:
        :return:
        """
        if int(prise) <= 0:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Так не получится...')
            await ctx.send(embed = emb, delete_after=20)
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
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{role.mention} успешно добавлена в магизин сервера!')
            await ctx.send(embed = emb)

    #измагаза-------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Измагазина', 'измагазина', 'измагаза', 'Измагаза'])
    async def del_shop_item(self, ctx, role: discord.Role):
        await ctx.channel.purge(limit=1)
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
        emb = discord.Embed(color = config.EMBED_COLOR, description = f'{role.mention} успешно удалена из магазина сервера!')
        await ctx.send(embed = emb)

    #магаз-------------------------------------------------
    @commands.command(aliases = ['Магазин', 'магазин', 'Магаз', 'магаз'])
    async def shop(self, ctx):
        prefix = self.get_prefix(self.cursor, ctx.message)
        await ctx.channel.purge(limit=1)
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
            emb.add_field(name='Роль:', value=f"{ctx.guild.get_role(item[1]).mention} - `{item[2]}` бублика", inline=False)
            emb.set_footer(text = f'❓ Купить {prefix}купить @роль')
        await ctx.send(embed = emb)

    #купить------------------------------------------------
    @commands.command(aliases = ['Купить', 'купить'])
    async def buy(self, ctx, role: discord.Role):
        await ctx.channel.purge(limit=1)
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
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(color=config.EMBED_COLOR_ERROR, title="Произошла ошибка!", description = "Такой роли `нет в магазине`")
            await ctx.send(embed = emb, delete_after=20)
        else:
            await ctx.channel.purge(limit=1)
            user_data = EconomicCogFunctionality.get_user_data(self.cursor, self.conn, ctx.message.author, ctx.guild)
            server = ctx.guild
            if user_data[3] < int(balance):
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f'{ctx.message.author.mention} Вы не можете купить {role.mention}\nУ вас `нет такой суммы` денег!')
                await ctx.send(embed = emb, delete_after=20)
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
                emb = discord.Embed(color = config.EMBED_COLOR, description = f'{ctx.message.author.mention}, вы получили {role.mention}!')
                await ctx.send(embed = emb)

def setup(client):
    """
    :param client:
    :return:
    """
    client.add_cog(EconomyCog(client))

