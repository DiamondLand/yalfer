import asyncio
import itertools
import sqlite3


import discord
import discord.ext.commands as commands
from config import config
from .music_player import MusicPlayer
from .music_utils import InvalidVC, VCError, YTDLSource


class Music(commands.Cog, name="Music"):

    __slots__ = ("bot", "players")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}
        self.connection = sqlite3.connect("database.db", timeout=10)
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

    async def cleanup(self, guild):

        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx: commands.Context):

        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx: commands.Context, error):

        if isinstance(error, commands.NoPrivateMessage):
            try:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Доступ к данному голосовому каналу запрещён')
                await ctx.reply(embed = emb, delete_after = 15)
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVC):
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = 'Невозможно подключиться к данному голосовому каналу')
            await ctx.reply(embed = emb, delete_after = 15)

    def get_player(self, ctx: commands.Context):

        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(aliases=["войти", "Войти"])
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        prefix = self.get_prefix(self.cursor, ctx.message)
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Сперва необходимо:', description = f'Добавить бота в голосовой канал `{prefix}войти <войс>`\nПодключиться самому')
                await ctx.reply(embed = emb, delete_after = 15)
                raise AttributeError(emb)

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Сбой подключения:', description = f'Подключение к `{channel}` было прервано')
                emb.set_footer(text=f"❓ Время ожидания истекло")
                await ctx.reply(embed = emb)
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Сбой подключения:', description = f'Подключение к `{channel}` было прервано')
                emb.set_footer(text=f"❓ Время ожидания истекло")
                await ctx.reply(embed = emb)

    @commands.command(aliases=["Р", "р", "p", "P", "п", "П", "плей", "Плей", "плэй", "Плэй"])
    async def play(self, ctx: commands.Context, *, search: str = None):
        await ctx.trigger_typing()
        await ctx.channel.purge(limit=1)

        if not search:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Сбой воспроизведения:', description = f'Запрос не был распознан корректно.\nВы можете повторить попытку')
            await ctx.send(embed = emb, delete_after = 15)
        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect)

        player = self.get_player(ctx)
        source = await YTDLSource.create_source(
            ctx, search, loop=self.bot.loop, download=False
        )

        await player.queue.put(source)

    @commands.command(aliases=["ps", "пауза", "Пауза"])
    async def pause(self, ctx: commands.Context):

        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)
        elif vc.is_paused():
            return

        vc.pause()
        author = ctx.author
        embed = discord.Embed(
            title=f"🎧 Пауза",
            description=f"⏸️ Остановил: {author.mention}",
            color = config.EMBED_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["r", 'продолжить', 'Продолжить'])
    async def resume(self, ctx: commands.Context):

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'Ошибка взаимодействия')
            emb.set_footer(text=f"❓ Возможно, в данный момент нет песен, находящихся на паузе")
            await ctx.send(embed = emb, delete_after = 15)

        elif not vc.is_paused():
            return

        vc.resume()
        author = ctx.author
        embed = discord.Embed(
            title=f"🎧 Воспроизведение",
            description=f"▶️ Снял с паузы: {author.mention}",
            color = config.EMBED_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["s", "Скип", "скип"])
    async def skip(self, ctx: commands.Context):
        prefix = self.get_prefix(self.cursor, ctx.message)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        player = self.get_player(ctx)
        if player.queue.empty():
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'На данный момент `нет` плейлиста')
            emb.set_footer(text=f"❓ Создайте его, находя интересующие треки {prefix}плей <название>")
            await ctx.send(embed = emb, delete_after = 15)
        else:
            vc.stop()
            author = ctx.author
            embed = discord.Embed(
                title=f"🎧 Скип",
                description=f"⏭️ Пропустил песню: {author.mention}",
                color = config.EMBED_COLOR,            
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["q", "Плейлист", "плейлист", "Плэйлист", "плэйлист", "Очередь", "очередь"])
    async def queue(self, ctx: commands.Context):
        prefix = self.get_prefix(self.cursor, ctx.message)
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)
        else:
            player = self.get_player(ctx)
            if player.queue.empty():
                await ctx.channel.purge(limit=1)
                emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'На данный момент нет `плейлиста`')
                emb.set_footer(text=f"❓ Создайте его, находя интересующие треки {prefix}плей <название>")
                await ctx.send(embed = emb, delete_after = 15)
            else:
                upcoming = list(itertools.islice(player.queue._queue, 0, 5))

                fmt = "\n\n".join(
                    f'➡️ **{i + 1}**: {song["title"]}' for i, song in enumerate(upcoming)
                )
                embed = discord.Embed(
                    title=f"🎧 Плейлист | `{len(upcoming)}`",
                    description=fmt,
                    color = config.EMBED_COLOR,
                )

                embed.set_footer(text=f"❓ Вы можете пропустить песню {prefix}скип")
                await ctx.send(embed=embed)

    @commands.command(aliases=["np", "Песня", "песня"])
    async def nowplaying(self, ctx: commands.Context):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)

        player = self.get_player(ctx)
        if not player.current:
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed(
            title=f"🎧 Сейчас играет:",
            description=f"`{vc.source.title}`",
            color = config.EMBED_COLOR,
        )
        embed.set_footer(
                    text=f"🎵 Поставил {vc.source.requester.name}"
                )

        player.np = await ctx.send(embed=embed)

    @commands.command(aliases=["vol", "Громкость", "громкость"])
    async def volume(self, ctx: commands.Context, *, vol: float):
        vc: discord.VoiceProtocol = ctx.voice_client

        if not vc or not vc.is_connected():
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'Ошибка взаимодействия')
            emb.set_footer(text=f"❓ Возможно, нет активного потока музыки.")
            await ctx.send(embed = emb, delete_after = 15)

        if not 0 < vol < 101:
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'Следует указать диапазон от `1` до `100`')
            await ctx.send(embed = emb, delete_after = 15)
            return

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        author = ctx.author
        embed = discord.Embed(
            title="🎧 Громкость изменена",
            description=f"🔊 {author.mention} изменил громкость на `{vol}%`",
            color = config.EMBED_COLOR,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["del", "Стоп", "стоп"])
    async def stop(self, ctx: commands.Context):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.channel.purge(limit=1)
            emb = discord.Embed(colour=config.EMBED_COLOR_ERROR, title='Оу!', description = f'На данный момент нет активного потока музыки')
            await ctx.send(embed = emb, delete_after = 15)
        await self.cleanup(ctx.guild)


#Cog-----------------------------------------------------
def setup(bot):
    bot.add_cog(Music(bot))
