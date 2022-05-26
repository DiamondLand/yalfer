# importing modules
import discord
import random
import sqlite3
import asyncio
from discord.ext import commands
from cogs.economic.economic import EconomicCogFunctionality
from cogs.economic.mining import MiningCogFunctionality


class MiningCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.prises = {
            "rtx 3090": "3293000",
            "RTX 3090": "3293000",
            "6900 xt": "2415000",
            "6900 XT": "2415000",
            "rtx 3080": "2735000",
            "6800 xt": "1679000",
            "rtx 3070": "1679000",
            "rtx 2080 ti": "1644000",
            "rtx a6000": "686000",
            "rx 6700 xt": "418222",
            "titan v": "407263",
            "rtx 2080": "402565",
            "rtx 2070": "389109",
            "rx 5700": "418291",
            "rtx 2060": "320491"
            }

        self.moneys_ = {
            "rtx 3090": "10932102",
            "RTX 3090": "10932102",
            "6900 xt": "1023503",
            "6900 XT": "1023503",
            "rtx 3080": "9839210",
            "6800 xt": "933221",
            "rtx 3070": "872129",
            "rtx 2080 ti": "522342",
            "rtx a6000": "421242",
            "rx 6700 xt": "676100",
            "titan v": "616200",
            "rtx 2080": "636400",
            "rtx 2070": "629300",
            "rx 5700": "619420",
            "rtx 2060": "593020"
        }
        self.chances_to_broke = [
            12, 22, 22, 18, 18, 24, 41, 55, 65, 73, 45, 15, 18, 57, 23
        ]
        self.videocards_companies = [
            "NVidia", "AMD", "AMD", "NVidia", "NVidia", "AMD", "NVidia", "NVidia", "NVidia", "AMD", "NVidia", "NVidia", "NVidia", "AMD", "NVidia"
        ]
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @commands.command(aliases = ['Майнинг', 'майнинг'])
    async def m_info(self, ctx):
        await ctx.send(
            file=discord.File(fp="video_card_ferm_2.png")
        )

    @commands.command(aliases = ['Мкупить', 'мкупить'])
    async def m_buy(self, ctx, *videocard_words):
        videocard = " ".join(videocard_words)
        if not (videocard in list(self.prises.keys())):
            emb = discord.Embed(colour = discord.Color.red(), description = 'Такой видеокарты `не существует`!')
            await ctx.send(embed = emb)
        else:
            user_data = EconomicCogFunctionality.get_user_data(
                self.cursor,
                self.connection,
                ctx.message.author,
                ctx.guild
            )
            wallet = user_data[3]
            member = ctx.message.author
            server = ctx.guild
            prise = int(self.prises[videocard])

            if prise > wallet:
                emb = discord.Embed(colour = discord.Color.red(), description = 'У вас нет такой суммы!')
                await ctx.send(embed = emb)
            else:
                MiningCogFunctionality.add_videocard(
                    videocard,
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
                emb = discord.Embed(colour = discord.Color.green(), description = ':white_check_mark: Успешно!')
                await ctx.send(embed = emb)


    @commands.command(aliases = ['Мферма', 'мферма'])
    async def m_my_farm(self, ctx):
        self.cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
            (
                ctx.guild.id,
                ctx.message.author.id
            )
        )
        result = self.cursor.fetchall()
        embed = discord.Embed(
            title=f"Майнинг ферма пользователя {ctx.message.author.name}!",
            color=0x00AAFF
        )
        embed.set_thumbnail(
            url=ctx.message.author.avatar_url
        )
        for element in result:
            if element[3] != 0:
                embed.add_field(
                    name=f"Видеокарты {element[2].title()}:",
                    value=f"Количество: {element[3]}\nПроизводитель: {self.videocards_companies[list(self.prises.keys()).index(element[2])]}"
                )
        await ctx.send(embed=embed)

    @commands.command(aliases = ['Мстоп', 'мстоп'])
    async def m_end(self, ctx):
        MiningCogFunctionality.DB_mining_set(
            ctx=ctx,
            cursor=self.cursor,
            connection=self.connection,
            value=False
        )
        emb = discord.Embed(colour = discord.Color.green(), description = ':white_check_mark: Сессия завершена!')
        await ctx.send(embed = emb)

    @commands.command(aliases = ['Мстарт', 'мстарт'])
    async def m_start(self, ctx):
        self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
                            (ctx.guild.id, ctx.message.author.id))
        is_mining_data = self.cursor.fetchone()
        if is_mining_data is None:
            pass
        elif is_mining_data[2] == 0:
            pass
        else:
            emb = discord.Embed(colour = discord.Color.red(), description = 'Вы уже майните! Остановка предыдущей сессии...')
            await ctx.send(embed = emb)
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
        emb = discord.Embed(colour = discord.Color.blurple(), description = 'Проверка...')
        discord_message =  await ctx.send(embed = emb)
        await asyncio.sleep(5)
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
            embed = discord.Embed(
                title=f"Майнинг ферма пользователя {ctx.message.author.name}!",
                color=0x00AAFF
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
                    ) / (6 * 60 * 24) * random.randint(1, 100) * element[3]
                    mined_moneys += mined_moneys_for_one
                    msg += f"Кэш: {round(mined_moneys_for_one, 2)}!\n"
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
                        msg += f"{amount_of_broken} видеокарт сломано\n"
                        MiningCogFunctionality.delete_videocards(
                            element[2],
                            amount_of_broken,
                            ctx.guild,
                            ctx.message.author,
                            self.cursor,
                            self.connection
                        )
                    embed.add_field(
                        name=f"Информация о сессии с видеокартами {element[2].title()}:",
                        value=f"{msg}"
                    )
                    embed.set_footer(
                        text=f"Налог: {round(mined_moneys / 5, 2)} 💰\nСчет за электричество: {round(mined_moneys / 8, 2)} 💰"
                    )
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
            total_time += 40
            await asyncio.sleep(40)
            if total_time == 80:
                emb = discord.Embed(colour = discord.Color.red(), description = 'Время майнинга вышло! Перезапустите для продолжения')
                await ctx.send(embed = emb)
                MiningCogFunctionality.DB_mining_set(
                    ctx=ctx,
                    cursor=self.cursor,
                    connection=self.connection,
                    value=False
                )
                return


# setup for cog
def setup(client):
    client.add_cog(MiningCog(client))
