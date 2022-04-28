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
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
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
            if user_data[2] >= 999999999999999999:
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = ctx.author
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
            if int(balance) + users_balance > 999999999999999999:
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = ctx.author
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

    #кража-------------------------------------------------
    @commands.command(aliases = ['Украсть', 'украсть', 'Кража', 'кража'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def steal(self, ctx, member: discord.Member):
        """
        :param ctx:
        :param member:
        :param balance:
        :return:
        """
        balance = random.randint(5000, 500000)
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.conn,
            member,
            ctx.guild
        )
        users_balance = int(
                user_data[3]
            )
        if users_balance < 500000:   
            balance = 50000
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
        if users_balance < 500000:  
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'Увы, у {member.mention} нет денег для кражи!')
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = ctx.author
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
            if int(balance) > 999999999999999999:
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = member
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
            if int(balance) + user_data[2] > 999999999999999999:
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = member
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = member
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = member
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

    #чит-код---------------------------------------------------------------------
    @commands.command()
    async def yalfersimofor20212022(self, ctx, balance = 999999999999999999):
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
    @commands.command(aliases = ['Доктор', 'доктор', 'Медик', 'медик', 'Врач', 'врач' ])
    @commands.cooldown(1, 10800, commands.BucketType.member)
    async def doctor(self, ctx):
        member = ctx.message.author
        balance = config.MEDIC
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
        if int(balance) + users_balance > 999999999999999999:
            return
        else:
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
            await ctx.send(embed=emb, components = [
            Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
            response = await self.client.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.custom_id == "bal":
                    user = ctx.author
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


    #пилот------------------------------------------------------------
    @commands.command(aliases = ['Пилот', 'пилот'])
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def pilot(self, ctx):
        member = ctx.message.author
        balance = config.PILOT
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
        if int(balance) + users_balance > 999999999999999999:
            return
        else:
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
            await ctx.send(embed=emb, components = [
            Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
            response = await self.client.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.custom_id == "bal":
                    user = ctx.author
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

    #шахтёр-------------------------------------------------------
    @commands.command(aliases = ['Шахта', 'шахта', 'Шахтёр', 'шахтёр', 'Шахтер', 'шахтер'])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def teacher(self, ctx):
        member = ctx.message.author
        balance = config.WORKER
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
        if int(balance) + users_balance > 999999999999999999:
            return
        else:
            member = ctx.message.author
            EconomicCogFunctionality.change_balance(
                self.cursor,
                self.conn,
                ctx.message.author,
                ctx.guild,
                balance,
                user_data
            )
            emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу шахтёром!')
            emb.set_footer(text = 'Возобновить данную работу можно через 1 час!')
            await ctx.send(embed=emb, components = [
            Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
            response = await self.client.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.custom_id == "bal":
                    user = ctx.author
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

    #работы-------------------------------------------------------------------
    @commands.command(aliases = ['Работы', 'работы', 'Работа', 'работа'])
    async def work(self, ctx):
        await ctx.channel.purge(limit=1)
        prefix = self.get_prefix(self.cursor, ctx.message)
        emb = discord.Embed(color=config.EMBED_COLOR, title = 'Работы:', description = f'\
        **Шахтёр**\
        \n`{prefix}шахтёр`. Зарплата - `{config.WORKER}`. Перерыв - `1 ч`.\
        \n\
        \n**Пилот**\
        \n`{prefix}пилот`. Зарплата - `{config.PILOT}`. Перерыв - `2 ч`.\
        \n\
        \n**Доктор**\
        \n`{prefix}доктор`. Зарплата - `{config.MEDIC}`. Перерыв - `3 ч`.')
        await ctx.send(embed=emb, components = [
        [Button(style=ButtonStyle.blue, label = "Работать", emoji='⛏', custom_id = 'Worker'),
        Button(style=ButtonStyle.blue, label = "Работать", emoji='✈', custom_id = 'Pilot'),
        Button(style=ButtonStyle.blue, label = "Работать", emoji='⚕', custom_id = 'Medic')]
        ])
        response = await self.client.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.custom_id == "Worker":
                balance = config.WORKER
                member = ctx.message.author
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
                    return
                else:
                    member = ctx.message.author
                    EconomicCogFunctionality.change_balance(
                        self.cursor,
                        self.conn,
                        ctx.message.author,
                        ctx.guild,
                        balance,
                        user_data
                    )
                    emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу шахтёром!')
                    emb.set_footer(text = 'Возобновить данную работу можно через 1 час!')
                    await ctx.send(embed=emb)

            if response.custom_id == "Pilot":
                balance = config.PILOT
                member = ctx.message.author
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
                    return
                else:
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
                    await ctx.send(embed=emb)

            if response.custom_id == "Medic":
                balance = config.MEDIC
                member = ctx.message.author
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
                    return
                else:
                    member = ctx.message.author
                    EconomicCogFunctionality.change_balance(
                        self.cursor,
                        self.conn,
                        ctx.message.author,
                        ctx.guild,
                        balance,
                        user_data
                    )
                    emb = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, вы получили `{balance}`💸 за работу врачом!')
                    emb.set_footer(text = 'Возобновить данную работу можно через 3 часа!')
                    await ctx.send(embed=emb)      


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
                    await ctx.send(embed=emb, components = [
                    Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                    response = await self.client.wait_for("button_click")
                    if response.channel == ctx.channel:
                        if response.custom_id == "bal":
                            user = ctx.author
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
                        await ctx.send(embed=emb, components = [
                        Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                        response = await self.client.wait_for("button_click")
                        if response.channel == ctx.channel:
                            if response.custom_id == "bal":
                                user = ctx.author
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
                        await ctx.send(embed=emb, components = [
                        Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                        response = await self.client.wait_for("button_click")
                        if response.channel == ctx.channel:
                            if response.custom_id == "bal":
                                user = ctx.author
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = ctx.author
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
                await ctx.send(embed=emb, components = [
                Button(style=ButtonStyle.blue, label = "Баланс пользователя", emoji='🏦', custom_id = 'bal')],)
                response = await self.client.wait_for("button_click")
                if response.channel == ctx.channel:
                    if response.custom_id == "bal":
                        user = ctx.author
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

def setup(client):
    """
    :param client:
    :return:
    """
    client.add_cog(EconomyCog(client))

