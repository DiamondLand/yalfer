import discord
import json
import os.path
import sqlite3
from loguru import logger
from discord.ext import commands
from config import config

class CustomCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.bot.logger = logger

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
        server_id = msg.guild
        file_path = f"custom/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"custom/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass

        file_path = f"warnings/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"warnings/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass
        
        with open(f'custom/{server_id}.json', 'r') as json_file:
            castom_commands = json.load(json_file)

        if castom_commands and (msg.content[1:] in castom_commands.keys()):
            embed = discord.Embed(colour=config.EMBED_COLOR, title = '💡 Кастомная команда:', description = castom_commands[msg.content[1:]])
            await msg.reply(embed = embed, mention_author=False)
            return


    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['Команда', 'команда'])
    async def add_command(self, ctx, name, *, reply):
        server_id = ctx.guild
        file_path = f"custom/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"custom/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass
        if (name is None) or (not reply):
            return
        server_id = ctx.guild
        with open(f'custom/{server_id}.json', 'r', encoding='utf-8') as json_file:
            all_commands = json.load(json_file)

        all_commands[name] = reply

        with open(f'custom/{server_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(all_commands, json_file)

        embed = discord.Embed(color=config.EMBED_COLOR, title="💎 Кастомная команда:", description=f"> Команда `{name}` внесена в список команд!")
        embed.add_field(name='🔮 Реагирование на команду: ', value=f"> {reply}")
        await ctx.reply(embed=embed, mention_author=False)


    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['Удалком', 'удалком'])
    async def delete_command(self, ctx, name):
        server_id = ctx.guild
        file_path = f"custom/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"custom/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass
        with open(f'custom/{server_id}.json', 'r', encoding='utf-8') as json_file:
            all_commands = json.load(json_file)

        if name not in all_commands.keys():
            embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, title = '❌ Ошибка:', description = f'Команда `{name}` не существует!')
            await ctx.reply(embed = embed, mention_author=False)
            return

        all_commands.pop(name)
        with open(f'custom/{server_id}.json', 'w', encoding='utf-8') as json_file:
            json.dump(all_commands, json_file)

        embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, title = '🎩 Кастомная команда:', description = f'> Команда `{name}` удалена из списка команд!')
        await ctx.reply(embed = embed, mention_author=False)
    
    @commands.command(aliases=['Кастом', 'кастом'])
    async def custom_commands(self, ctx):
        server_id = ctx.guild
        file_path = f"custom/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"custom/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass
        with open(f"custom/{server_id}.json", 'r', encoding='utf-8') as json_file:
            all_servers = json.load(json_file)


        if all_servers:
            emb = discord.Embed(color=config.EMBED_COLOR, title=f"🧷 Кастомные команды для {ctx.guild}:")
            for command in all_servers.keys():
                emb.add_field(name=command, value=all_servers[command], inline=False)
        else:
            emb = discord.Embed(color=config.EMBED_COLOR_WHAT, title="💛 Нет, нет, нет!", description=f"На сервере **{ctx.guild}** отсутствуют кастомные команды!")
        await ctx.reply(embed=emb, mention_author=False)

def setup(bot):
    bot.add_cog(CustomCommands(bot))



