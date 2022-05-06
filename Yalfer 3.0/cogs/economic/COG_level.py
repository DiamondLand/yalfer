import discord
import sqlite3
from discord.ext import commands
from config import config

class LevelSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

    @commands.Cog.listener()
    async def on_message(self, msg):
        msg_author = msg.author

        if msg_author == self.client.user:
            return

        msg_guild = msg.guild
        length = len(msg.content)

        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()

        if data == None:
            self.cursor.execute(
                "INSERT INTO server_activity VALUES (?, ?, 0, 0)",
                (
                    msg_guild.id,
                    msg_author.id
                )
            )
            self.conn.commit()
            return

        current_server_activity = data[2]
        current_server_level = data[3]

        current_server_activity += length
        new_server_level = int(
            current_server_activity / 4000
        )

        if new_server_level != current_server_level:
            await msg.channel.send(
                f"{msg_author.mention}, вы получили  `{new_server_level}` уровень!"
            )

        self.cursor.execute(
            "UPDATE server_activity SET user_server_activity = ?, user_level = ? WHERE guild_id = ? AND member_id = ?",
            (
                current_server_activity,
                new_server_level,
                msg_guild.id,
                msg_author.id
            )
        )
        self.conn.commit()

    @commands.command(aliases = ['Лвл', 'лвл', 'Уровень', 'уровень'])
    async def level(self, ctx, member: discord.Member = None):
        if member == None:
            msg_author = ctx.message.author
        else:
            msg_author = member

        msg_guild = ctx.guild
        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()
        if data == None:
            level = 0
            activity = 0
            return
        else:
            level = data[3]
            activity = data[2]
        embed = discord.Embed(title = f"Уровень на сервере {msg_author.name}:", color = config.EMBED_COLOR)
        not_done = (((data[3] + 1) * 2000) - (data[2]))
        done = 2000 - not_done
        print(done, not_done)
        embed.add_field(name = "Текущий уровень: ", value = str(level) + " ✅", inline = False)
        embed.add_field(name = "Очки активности: ", value = str(activity) + " 🕐", inline = False)
        embed.add_field(name = "Сколько осталось до следующего уровня: ", value = ":green_square:" * int(done / 200) + ":yellow_square:" * int(not_done / 200) + f" ({done / 20} %)", inline = False)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed = embed)


    @commands.command(aliases = ['Лвлденьги', 'лвлденьги'])
    async def activity_to_moneys(self, ctx, levels: int):
        msg_author = ctx.message.author
        length = len(ctx.message.content)
        msg_guild = ctx.guild
        self.cursor.execute(
            "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
            (
                msg_guild.id,
                msg_author.id
            )
        )
        data = self.cursor.fetchone()
        if (data[3] < levels):
            await ctx.send(
                "У вас нет столько уровней!"
            )
        else:
            self.cursor.execute(
                "SELECT * FROM server_activity WHERE guild_id = ? AND member_id = ?",
                (
                    msg_guild.id,
                    msg_author.id
                )
            )
            data = self.cursor.fetchone()
            current_server_activity = data[2]
            current_server_level = data[3]
            current_server_activity -= levels * 2000
            new_server_level = current_server_level - levels
            self.cursor.execute(
                "UPDATE server_activity SET user_server_activity = ?, user_level = ? WHERE guild_id = ? AND member_id = ?",
                (
                    current_server_activity,
                    new_server_level,
                    msg_guild.id,
                    msg_author.id
                )
            )
            self.conn.commit()
            user_data = self.get_user_data(msg_author, ctx.guild)
            server = ctx.guild
            self.cursor.execute(
                "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
                (
                    user_data[3] + (levels ** 3) * 1000,
                    msg_author.id,
                    server.id
                )
            )
            self.conn.commit()
            await ctx.send(
                f"You got {(levels ** 2) * 1000} 💸. (Level ^ 3 * 1000)"
            )

    def get_user_data(self, member, server):
        self.cursor.execute(
            "SELECT * FROM economic WHERE member_id = ? AND guild_id = ?",
            (
                member.id,
                server.id
            )
        )
        data = self.cursor.fetchone()
        if data is None:
            self.cursor.execute(
                "INSERT INTO economic VALUES (?, ?, 0, 0)",
                (
                    server.id,
                    member.id
                )
            )
            self.conn.commit()
            data = self.cursor.fetchone()
            return (
                server.id,
                member.id,
                0,
                0
            )
        return data


def setup(client):
    client.add_cog(LevelSystem(client))
