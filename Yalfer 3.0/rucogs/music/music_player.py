import asyncio
import discord

from async_timeout import timeout
from discord.ext import commands
from config import config
from .music_utils import YTDLSource


class MusicPlayer:

    __slots__ = (
        "bot",
        "_guild",
        "_channel",
        "_cog",
        "queue",
        "next",
        "current",
        "np",
        "volume",
    )

    def __init__(self, ctx: commands.Context):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.np = None 
        self.volume = 0.5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(
                        source, loop=self.bot.loop
                    )
                except Exception as e:
                    emb = discord.Embed(colour=config.EMBED_COLOR, title='Произошла ошибка!', description = f':no_entry_sign: {e}')
                    await self._channel.send(embed = emb, delete_after = 15)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )

            embed = discord.Embed(
                title=f"🎧 Сейчас играет:",
                description=f"`{source.title}`",
                color = config.EMBED_COLOR,
            )
            embed.set_footer(
                    text=f"🎵 Поставил: {source.requester.name}"
                )

            self.np = await self._channel.send(embed=embed)

            await self.next.wait()

            try:
                source.cleanup()
            except ValueError as ex:
                error_embed = discord.Embed(
                    title="👎 Discord.py Error",
                    description=f"🐍 Discord.py\n`{ex.args}`",
                    color = config.EMBED_COLOR_ERROR,
                )

                error_embed.set_footer(
                    text="❓ Устаревшая версия Yalfer"
                )

                await self._channel.send(embed=error_embed)

            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))
