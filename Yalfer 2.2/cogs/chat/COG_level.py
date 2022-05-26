import discord
import sqlite3
from config import config
from discord.ext import commands


class LevelSystem(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect(
            "database.db"
        )
        self.cursor = self.conn.cursor()

    def get_prefix(self, cursor, message):
        cursor.execute(
            "SELECT * FROM prefixes WHERE guild_id = ?", 
            (
                message.guild.id
            )
        )
        result = cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return "+"

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
            current_server_activity / 1700
        )

        if new_server_level != current_server_level:
           embed = discord.Embed(description = f"{msg_author.mention} повышен на `{new_server_level}` уровень!", color=config.EMBED_COLOR)
           await msg.channel.send(embed=embed)
          

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
        embed = discord.Embed(title = f"Активность {msg_author.name}:", color=config.EMBED_COLOR)
        not_done = (((data[3] + 1) * 1700) - (data[2]))
        done = 1700 - not_done
        print(done, not_done)
        embed.add_field(name = "Уровень: ", value = str(level) + " ✅", inline = False)
        embed.add_field(name = "Очки активности: ", value = str(activity) + " 🕐", inline = False)
        embed.add_field(name = "До следующего уровня: ", value = ":green_square:" * int(done / 200) + ":red_square:" * int(not_done / 200) + f" ({done / 20} %)", inline = False)
        embed.set_thumbnail(url = msg_author.avatar_url)
        await ctx.send(embed = embed)


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
