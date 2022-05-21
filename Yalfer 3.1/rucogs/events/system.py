import json
import requests
import discord
from config import config

class EventsCogFunctionality:
    
    @staticmethod
    def get_all_items(cursor, guild):
        return cursor.execute(
            """
            SELECT * FROM server_for_members WHERE guild_id = ?
            """,
                              (
                                  guild.id,
                              )
                              ).fetchall()