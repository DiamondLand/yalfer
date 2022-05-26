import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
from config import config

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '`{0.title}`'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Не удалось найти ничего подходящего `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Не удалось найти ничего подходящего `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Не удалось найти ничего подходящего `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Не удалось найти никаких совпадений для `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('**{}** д'.format(days))
        if hours > 0:
            duration.append('**{}** ч'.format(hours))
        if minutes > 0:
            duration.append('**{}** мин'.format(minutes))
        if seconds > 0:
            duration.append('**{}** сек'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Сейчас играет', url= '{0.source.url}'.format(self), description='`{0.source.title}\n`'.format(self) + f'{self.source.duration}', color=config.EMBED_COLOR)
                 .add_field(name='Поставил:', value=self.requester.mention)
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180):
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

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

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Эту команду невозможно использовать в данном чате')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    @commands.command(name='join', aliases = ['Войти', 'войти'], invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon', aliases = ['Ксебе', 'ксебе'])
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        await ctx.channel.purge(limit=1)
        if not channel and not ctx.author.voice:
            raise VoiceError('Вы не подключены к голосовому каналу и не указали канал для подключения')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['Выйти', 'выйти'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.voice:
            return await ctx.send('Бот не подключен к голосовому каналу', delete_after=10)

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume', aliases=['З', 'з', 'Звук', 'звук', 'Громкость', 'громкость'])
    async def _volume(self, ctx: commands.Context, *, volume: int):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.is_playing:
            return await ctx.send('В данный момент нет активного потока.', delete_after=10)
        ctx.voice_state.volume = volume / 100
        await ctx.send('Громкость установлена на `{}`%'.format(volume), delete_after=10)

    @commands.command(name='now', aliases=['Сейчас', 'сейчас', 'Песня', 'песня'])
    async def _now(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', aliases=['Пауза', 'пауза'])
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume', aliases=['Продолжить', 'продолжить'])
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop0', aliases=['O0','o0', 'О0','о0', 'Очередь0', 'очередь0', 'Плейлист0', 'плейлист0', 'Плэйлист0', 'плэйлист0'])
    @commands.has_permissions(manage_guild=True)
    async def _stop0(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip', aliases=['C', 'c', 'С', 'с' 'Скип', 'скип'])
    async def _skip(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('В данный момент нет активного потока', delete_after=10)

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Голосование за пропуск `{}/3`'.format(total_votes), delete_after=15)

        else:
            await ctx.send('Вы уже проголосовали.', delete_after=10)

    @commands.command(name='queue', aliases = ['O','o', 'О','о', 'Очередь', 'очередь', 'Плейлист', 'плейлист', 'Плэйлист', 'плэйлист'])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        await ctx.channel.purge(limit=1)
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Пусто...', delete_after=10)

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '[{1.source.title}]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(color=config.EMBED_COLOR, description='`{}` Трек(-ов)\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Страница {}/{}'.format(page, pages)))
        await ctx.send(embed=embed, delete_after=20)

    @commands.command(name='loop', aliases = ['Ц', 'ц', 'Цикл', 'цикл'])
    async def _loop(self, ctx: commands.Context):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.is_playing:
            return await ctx.send('В данный момент нет активного потока.', delete_after=10)

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', aliases = ['P', 'p', 'п', 'П', 'Плей', 'плей', 'Плэй', 'плэй'])
    async def _play(self, ctx: commands.Context, *, search: str):
        await ctx.channel.purge(limit=1)
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)
            await ctx.channel.purge(limit=1)
        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('При обработке этого запроса произошла ошибка: `{}`'.format(str(e)), delete_after=10)
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send(':track_next:  {}'.format(str(source)), delete_after=60)
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('Вы не подключены к каналу')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Бот не в канале')



def setup(bot):
   bot.add_cog(Music(bot))


