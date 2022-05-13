import discord
import random
import sqlite3
import asyncio
import time
from discord.ext import commands
from cogs.economic.system import EconomicCogFunctionality
from cogs.economic.system import MiningCogFunctionality
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
from config import config


class MiningCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prises = {
            "rtx 3090": "85000000",
            "6900 xt": "65000000",
            "rtx 3080": "55000000",
            "6800 xt": "45000000",
            "rtx 3070": "35000000",
            "rtx 2080 ti": "25000000",
            "rtx a6000": "10000000",
            "rx 6700 xt": "7000000",
            "titan v": "8000000",
            "rtx 2080": "4000000",
            "rtx 2070": "1000000",
            "rx 5700": "500000",
            "rtx 2060": "200000"
            }

        self.moneys_ = {
            "rtx 3090": "85000000",
            "6900 xt": "65000000",
            "rtx 3080": "55000000",
            "6800 xt": "45000000",
            "rtx 3070": "35000000",
            "rtx 2080 ti": "25000000",
            "rtx a6000": "10000000",
            "rx 6700 xt": "7000000",
            "titan v": "8000000",
            "rtx 2080": "4000000",
            "rtx 2070": "1000000",
            "rx 5700": "500000",
            "rtx 2060": "200000"
            }
        self.chances_to_broke = [
            12, 13, 8, 17, 8, 9, 11, 2, 14, 10, 18, 47, 50
        ]
        self.videocards_companies = [
            "NVidia", "AMD", "NVidia", "AMD", "NVidia", "NVidia", "NVidia", "NVidia", "AMD", "NVidia", "NVidia", "AMD", "NVidia"
        ]
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @commands.command(aliases = ['Млист', 'млист'])
    async def m_info(self, ctx):
        await ctx.send(components = [
            Select(
                placeholder = "Выбери видюху:",
                options = [
                    SelectOption(label = "rtx 3090", value = "rtx 3090"),
                    SelectOption(label = "6900 xt", value = "6900 xt"),
                    SelectOption(label = "rtx 3080", value = "rtx 3080"),
                    SelectOption(label = "6800 xt", value = "6800 xt"),
                    SelectOption(label = "rtx 3070", value = "rtx 3070"),
                    SelectOption(label = "rtx 2080 ti", value = "rtx 2080 ti"),
                    SelectOption(label = "rtx a6000", value = "rtx a6000"),
                    SelectOption(label = "rx 6700 xt", value = "rx 6700 xt"),
                    SelectOption(label = "titan v", value = "titan v"),
                    SelectOption(label = "rtx 2080", value = "rtx 2080"),
                    SelectOption(label = "rtx 2070", value = "rtx 2070"),
                    SelectOption(label = "rx 5700", value = "rx 5700"),
                    SelectOption(label = "rtx 2060", value = "rtx 2060")
                ]
            )
        ],)

        embed1 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 3090', description = 'Цена видеокарты: `85.000.000`\nВероятность поломки: `12%`\nОценка: `5/5`')
        embed2 = discord.Embed(colour=config.EMBED_COLOR, title = '6900 xt', description = 'Цена видеокарты: `65.000.000`\nВероятность поломки: `13%`\nОценка: `5/5`')
        embed3 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 3080', description = 'Цена видеокарты: `55.000.000`\nВероятность поломки: `8%`\nОценка: `5/5`')
        embed4 = discord.Embed(colour=config.EMBED_COLOR, title = '6800 xt', description = 'Цена видеокарты: `45.000.000`\nВероятность поломки: `17%`\nОценка: `4.5/5`')
        embed5 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 3070', description = 'Цена видеокарты: `35.000.000`\nВероятность поломки: `20%`\nОценка: `4.2/5`')
        embed6 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 2080 ti', description = 'Цена видеокарты: `25.000.000`\nВероятность поломки: `9%`\nОценка: `4.2/5`')
        embed7 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx a6000', description = 'Цена видеокарты: `10.000.000`\nВероятность поломки: `11%`\nОценка: `5/5`')
        embed8 = discord.Embed(colour=config.EMBED_COLOR, title = 'rx 6700 xt', description = 'Цена видеокарты: `8.000.000`\nВероятность поломки: `2%`\nОценка: `5/5`')
        embed9 = discord.Embed(colour=config.EMBED_COLOR, title = 'titan v', description = 'Цена видеокарты: `7.000.000`\nВероятность поломки: `14%`\nОценка: `5/5`')
        embed10 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 2080', description = 'Цена видеокарты: `4.000.000`\nВероятность поломки: `10%`\nОценка: `3.4/5`')
        embed11 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 2070', description = 'Цена видеокарты: `1.000.000`\nВероятность поломки: `18%`\nОценка: `3/5`')
        embed12 = discord.Embed(colour=config.EMBED_COLOR, title = 'rx 5700', description = 'Цена видеокарты: `500.000`\nВероятность поломки: `47%`\nОценка: `2.5/5`')
        embed13 = discord.Embed(colour=config.EMBED_COLOR, title = 'rtx 2060', description = 'Цена видеокарты: `200.000`\nВероятность поломки: `50%`\nОценка: `2.5/5`')

        while True:
            try:
                event = await self.client.wait_for("select_option", check=None)
                label = event.values[0]
                if label == "rtx 3090":
                    await event.respond(embed = embed1, ephemeral=True)
                elif label == "6900 xt":
                    await event.respond(embed = embed2, ephemeral=True)
                elif label == "rtx 3080":
                    await event.respond(embed = embed3, ephemeral=True)
                elif label == "6800 xt":
                    await event.respond(embed = embed4, ephemeral=True)
                elif label == "rtx 3070":
                    await event.respond(embed = embed5, ephemeral=True)
                elif label == "rtx 2080 ti":
                    await event.respond(embed = embed6, ephemeral=True)
                elif label == "rtx a6000":
                    await event.respond(embed = embed7, ephemeral=True)
                elif label == "rx 6700 xt":
                    await event.respond(embed = embed8, ephemeral=True)
                elif label == "titan v":
                    await event.respond(embed = embed9, ephemeral=True)
                elif label == "rtx 2080":
                    await event.respond(embed = embed10, ephemeral=True)
                elif label == "rtx 2070":
                    await event.respond(embed = embed11, ephemeral=True)
                elif label == "rx 5700":
                    await event.respond(embed = embed12, ephemeral=True)
                elif label == "rtx 2060":
                    await event.respond(embed = embed13, ephemeral=True)

            except discord.NotFound:
                print("error.")

    @commands.command(aliases = ['Мкупить', 'мкупить'])
    async def m_buy(self, ctx, *videocard_words):
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.prises.keys())):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Данная видеокарта не существует!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.connection,
                ctx.message.author,
                ctx.guild
            )
            wallet = user_data[3]
            author = ctx.message.author
            member = ctx.message.author
            server = ctx.guild
            prise = int(self.prises[videocard])
            if prise > wallet:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'У Вас отсутствует данная сумма!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                MiningCogFunctionality.add_videocard(
                    videocard,
                    1,
                    server,
                    member,
                    self.cursor,
                    self.connection
                )
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.connection,
                    ctx.message.author,
                    ctx.guild,
                    - prise,
                    user_data
                )
                emb = discord.Embed(colour=config.EMBED_COLOR, title=f"Аккаунт {ctx.author}:", description = f'💖 Приобрёл `{videocard}`!')
                await ctx.reply(embed = emb, mention_author=False)

    @commands.command(aliases = ['Мпродать', 'мпродать'])
    async def m_sold(self, ctx, *videocard_words):
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.moneys_.keys())):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = 'Данная видеокарта не существует или же отстутствует у Вас!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.connection,
                ctx.message.author,
                ctx.guild
            )
            server = ctx.guild
            prise = int(self.prises[videocard])
            users_balance = int(
                user_data[3]
            )
            if int(prise) + users_balance > 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_WHAT, title="💛 Изъятие:", description = 'Брат, брат, брат. У тебя слишком много денег. Видеокарта была изъята!')
                await ctx.reply(embed = emb, mention_author=False)
                MiningCogFunctionality.delete_videocards(
                        videocard,
                        1,
                        server,
                        ctx.message.author,
                        self.cursor,
                        self.connection
                    )
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
            else:
                MiningCogFunctionality.delete_videocards(
                        videocard,
                        1,
                        server,
                        ctx.message.author,
                        self.cursor,
                        self.connection
                    )
                EconomicCogFunctionality.change_balance(
                        self.cursor,
                        self.connection,
                        ctx.message.author,
                        ctx.guild,
                        + prise,
                        user_data
                )
                emb = discord.Embed(colour=config.EMBED_COLOR, title=f"Аккаунт {ctx.author}:", description = f'💖 Продал `{videocard}` за `{prise}`!')
                await ctx.reply(embed = emb, mention_author=False)
            
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Мубрать', 'мубрать'])
    async def m_remove(self, ctx, member: discord.Member, amount=1, *videocard_words):
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.moneys_.keys())):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'Данная видеокарта не существует или же отстутствует у {member.mention}!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            """
            :param ctx:
            :param member:
            :return:
            """
            MiningCogFunctionality.delete_videocards(
                    videocard,
                    amount,
                    ctx.guild,
                    member,
                    self.cursor,
                    self.connection
                )
            
            emb = discord.Embed(colour=config.EMBED_COLOR, title=f"Аккаунт {member}:", description = f'💔 Лишается `{videocard}`!')
            await ctx.reply(embed = emb, mention_author=False)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Мвыдать', 'мвыдать'])
    async def m_get(self, ctx, member: discord.Member, *videocard_words):
        member = member or ctx.author
        """
        :param ctx:
        :param member:
        :return:
        """
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.prises.keys())):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="❌ Ошибка:", description = f'Данная видеокарта не существует!')
            await ctx.reply(embed = emb, mention_author=False)
        else:
            MiningCogFunctionality.add_videocard(
                    videocard,
                    1,
                    ctx.guild,
                    member,
                    self.cursor,
                    self.connection,
            )      
            emb = discord.Embed(colour=config.EMBED_COLOR, title=f"Аккаунт {member}:", description = f'💖 Получил `{videocard}`!')
            await ctx.reply(embed = emb, mention_author=False)

    @commands.command(aliases = ['Мферма', 'мферма'])
    async def m_my_farm(self, ctx, author: discord.Member = None):
        author = author or ctx.author
        self.cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
            (
                ctx.guild.id,
                author.id
            )
        )
        result = self.cursor.fetchall()
        embed = discord.Embed(
            description=f"**Майнинг ферма** {author.mention}**:**",
            color=config.EMBED_COLOR
        )
        for element in result:
            if element[3] != 0:
                embed.add_field(
                    name=f"Видеокарты `{element[2].title()}`:",
                    value=f"Количество: `{element[3]}`\nПроизводитель: *{self.videocards_companies[list(self.prises.keys()).index(element[2])]}*"
                )
        await ctx.send(embed=embed)

    @commands.command(aliases = ['Мстарт', 'мстарт'])
    @commands.cooldown(1, 500, commands.BucketType.member)
    async def m_start(self, ctx):
        self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?", (ctx.guild.id, ctx.message.author.id))
        is_mining_data = self.cursor.fetchone()
        if is_mining_data is None:
            pass
        elif is_mining_data[2] == 0:
            pass
        else:
            emb = discord.Embed(colour=config.EMBED_COLOR_WHAT, title="💛 Процесс:", description = 'Брат, брат, брат. Ты уже майнишь! Останавливаю прошлую сессию...')
            await ctx.reply(embed = emb, mention_author=False)
            MiningCogFunctionality.DB_mining_set(
                ctx=ctx,
                cursor=self.cursor,
                connection=self.connection,
                value=False
            )
        MiningCogFunctionality.DB_mining_set(
            ctx=ctx,
            cursor=self.cursor,
            connection=self.connection,
            value=True
        )
        self.connection.commit()
        user_data = EconomicCogFunctionality.get_user_data(
            self.cursor,
            self.connection,
            ctx.message.author,
            ctx.guild
        )
        server = ctx.guild
        member = ctx.message.author
        emb = discord.Embed(colour=config.EMBED_COLOR_WHAT, title="💛 Процесс:", description = 'Выполняется проверка, ожидайте')
        discord_message = await ctx.reply(embed = emb, mention_author=False)
        await asyncio.sleep(3)
        mined_moneys = 0
        total_time = 0
        while True:
            self.cursor.execute(
                "SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
                (
                    server.id,
                    member.id
                )
            )
            is_mining_data = self.cursor.fetchone()
            if is_mining_data is None:
                return
            elif is_mining_data[2] == 0:
                return
            author = ctx.message.author
            embed = discord.Embed(
                description=f"**Майнинг ферма** {author.mention}**:**",
                color=config.EMBED_COLOR
            )
            embed.set_thumbnail(
                url=ctx.message.author.avatar_url
            )
            self.cursor.execute(
                "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
                (
                    ctx.guild.id,
                    ctx.message.author.id
                )
            )
            result = self.cursor.fetchall()
            for element in result:
                if element[3] != 0:
                    msg = ""
                    mined_moneys_for_one = int(
                        self.moneys_[element[2]]
                    ) / (3 * 9) * random.randint(1, 10) * element[3]
                    mined_moneys += mined_moneys_for_one
                    msg += f"Кэш: `{round(mined_moneys_for_one, 2)}`, растёт каждые *30* секунд!\n"
                    chances_to_broke = int(
                        self.chances_to_broke[list(self.prises.keys()).index(str(element[2]))]
                    )
                    un_chances = 100 - chances_to_broke
                    amount_of_broken = 0

                    for i in range(int(element[3])):
                        random_number = random.randint(0, un_chances)
                        another_random_number = random.randint(0, un_chances)
                        if (random_number == another_random_number):
                            amount_of_broken += 1

                    if amount_of_broken != 0:
                        msg += f"`{amount_of_broken}` видеокарт сломано\n"
                        MiningCogFunctionality.delete_videocards(
                            element[2],
                            amount_of_broken,
                            ctx.guild,
                            ctx.message.author,
                            self.cursor,
                            self.connection
                        )
                    embed.add_field(
                        name=f"Информация о сессии с видеокартами *{element[2].title()}*:",
                        value=f"{msg}"
                    )
                    embed.set_footer(
                        text=f"\n💎 Налог - {round(mined_moneys / 4, 2)} 💰\n💡 Счет за электричество - {round(mined_moneys / 8, 2)} 💰"
                    )
            users_balance = int(
                user_data[3]
            )
            if int(mined_moneys) + users_balance > 999999999999999999:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title="💛 Процесс:", description = 'Брат, брат, брат. У тебя слишком ного денег. Ты не можешь майнить!')
                await ctx.reply(embed = emb, mention_author=False)
            else:
                await discord_message.edit(embed=embed)
                EconomicCogFunctionality.change_balance(
                    self.cursor,
                    self.connection,
                    ctx.message.author,
                    ctx.guild,
                    + mined_moneys,
                    EconomicCogFunctionality.get_user_data(
                        self.cursor,
                        self.connection,
                        ctx.message.author,
                        ctx.guild,
                    )
                )
            total_time += 30
            await asyncio.sleep(30)
            if total_time == 60:
                author = ctx.message.author
                emb = discord.Embed(colour=config.EMBED_COLOR_WHAT, title="💛 Процесс:", description = f'{author.mention}, сессия была завершена!')
                await ctx.send(embed = emb)
                MiningCogFunctionality.DB_mining_set(
                    ctx=ctx,
                    cursor=self.cursor,
                    connection=self.connection,
                    value=False
                )
                
def setup(client):
    client.add_cog(MiningCog(client))
