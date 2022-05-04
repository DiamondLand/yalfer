import json
import requests
import discord
from config import config

class EconomicCogFunctionality:

    @staticmethod
    def get_user_data(cursor, conn, member, server):
        cursor.execute(
            "SELECT * FROM economic WHERE member_id = ? AND guild_id = ?",
            (
                member.id,
                server.id
            )
        )
        data = cursor.fetchone()
        if data is None:
            cursor.execute(
                "INSERT INTO economic VALUES (?, ?, 0, 0, 0)",
                (
                    server.id,
                    member.id
                )
            )
            conn.commit()
            data = cursor.fetchone()
            return server.id, member.id, 0, 0
        return data
        

    @staticmethod
    async def send_balance_info(ctx, member, data):
        embed = discord.Embed(
            description=f"**Баланс** {member.mention}:",
            color=config.EMBED_COLOR)
        embed.set_thumbnail(
            url=member.avatar_url
        )
        embed.add_field(
            name="Наличкой:",
            value=f"{data[3]} 💸"
        )
        embed.add_field(
            name="В банке:", value=f"{data[2]} 💰"
        )
        embed.add_field(
            name="Коины:", value=f"{data[4]} 🪙"
        )
        await ctx.send(
            embed=embed
        )

    @staticmethod
    def change_balance(cursor, conn, member, guild, balance: int, user_data):
        cursor.execute(
            "UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
            (
                int(user_data[3]) + int(balance),
                member.id,
                guild.id
            )
        )
        conn.commit()

    @staticmethod
    def change_bank_balance(cursor, conn, member, guild, balance: int, user_data):
        cursor.execute(
            "UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
            (
                user_data[2] + int(balance),
                member.id,
                guild.id
            )

        )
        conn.commit()

    @staticmethod
    def change_coin_balance(cursor, conn, member, guild, balance: int, user_data):
        cursor.execute(
            "UPDATE economic SET bank_balance = ? WHERE member_id = ? AND guild_id = ?",
            (
                user_data[4] + int(balance),
                member.id,
                guild.id
            )

        )
        conn.commit()

    @staticmethod
    def get_all_shop_items(cursor, guild):
        return cursor.execute(
            """
            SELECT * FROM economic_shop_item WHERE guild_id = ? ORDER BY prise
            """,
                              (
                                  guild.id,
                              )
                              ).fetchall()

class MiningCogFunctionality:

    @staticmethod
    def delete_videocards(videocard, amount, guild, member, cursor, connection):
        cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
            (
                guild.id,
                member.id,
                videocard
            )
        )
        result = cursor.fetchone()
        if result[3] < amount:
            amount = result[3]
        cursor.execute(
            "UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
            "graphics_cards_name = ?",
            (
                result[3] - amount,
                guild.id,
                member.id,
                videocard
            )
        )
        connection.commit()

    @staticmethod
    def add_videocard(videocard, amount, guild, member, cursor, connection):
        cursor.execute(
            "SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
            (
                guild.id,
                member.id,
                videocard
            )
        )
        result = cursor.fetchone()
        if result is None:
            cursor.execute(
                "INSERT INTO graphics_cards VALUES (?, ?, ?, ?)",
                (
                    guild.id,
                    member.id,
                    videocard,
                    amount
                )
            )
        else:
            cursor.execute(
                "UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
                "graphics_cards_name = ?",
                (
                    result[3] + amount,
                    guild.id,
                    member.id,
                    videocard
                )
            )
        connection.commit()
        return


    @staticmethod
    def DB_mining_set(cursor, connection, ctx, value: bool):
        cursor.execute(
            "DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?",
            (
                ctx.guild.id,
                ctx.message.author.id
            )
        )
        cursor.execute("INSERT INTO is_mining VALUES (?, ?, ?)",
                       (
                           ctx.guild.id,
                           ctx.message.author.id,
                           int(value)
                       )
                       )
        connection.commit()
