import discord
import sqlite3
import asyncio
import datetime
import json
import os
from config import config
from discord.ext import commands

class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db", timeout=10)
        self.cursor = self.connection.cursor()

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

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases = ['Варн', 'варн', 'Пред', 'пред'])
    async def warn(self, ctx, user: discord.Member, *, reason='Не указана'):
        server_id = ctx.guild
        file_path = f"warnings/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"warnings/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass

        with open(f"warnings/{server_id}.json", 'r') as json_file:
            all_users = json.load(json_file)

        if str(user.id) not in all_users.keys():
            all_users[str(user.id)] = [reason]
        else:
            user_warnings = all_users[str(user.id)]
            user_warnings.append(reason)

        with open(f"warnings/{server_id}.json", 'w') as json_file:
            json.dump(all_users, json_file)

        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'🚨 Варн:', description = f'{user.mention} получает варн!\
        \n> Причина: **{reason}**!')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'🚨 Варн:', description = f'Вы получили варн на сервере **{ctx.guild}**!\
        \n> Причина: **{reason}**!')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=user.avatar_url)
        await user.send(embed=embed)


    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases = ['Варны', 'варны', 'Преды', 'преды'])
    async def warns(self, ctx, user: discord.Member):
        server_id = ctx.guild
        file_path = f"warnings/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"warnings/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass

        with open(f"warnings/{server_id}.json", 'r') as json_file:
            all_users = json.load(json_file)

        embed = None
        if str(user.id) in all_users.keys():
            embed = discord.Embed(colour=config.EMBED_COLOR, title='🚨 Варны пользователя:', description=f'> {user.mention} имеет:')
            for i in range(len(all_users[str(user.id)])):
                embed.add_field(name=f'{str(i + 1)})', value=all_users[str(user.id)][i], inline=False)
        else:
            embed = discord.Embed(colour=config.EMBED_COLOR, title="🚨 Варны пользователя:", description=f"> {user.mention} не имеет варнов!")

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)


    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases = ['удалварн', 'Удалварн', 'удалпред', 'Удалпред'])
    async def clear_warnings(self, ctx, user: discord.Member):
        server_id = ctx.guild
        file_path = f"warnings/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"warnings/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass

        with open(f"warnings/{server_id}.json", 'r') as json_file:
            all_users = json.load(json_file)

        if str(user.id) not in all_users.keys():
            embed = discord.Embed(colour=config.EMBED_COLOR, title="🚨 Варны пользователя:", description=f"{user.mention} не имеет варнов!")
        else:
            all_users.pop(str(user.id))

            with open(f"warnings/{server_id}.json", 'w') as json_file:
                json.dump(all_users, json_file)
            embed = discord.Embed(colour=config.EMBED_COLOR, title="🚨 Варны пользователя:", description=f'Варны {user.mention} были очищены!')

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

#<<------------->>
def setup(bot):
   bot.add_cog(Warns(bot))