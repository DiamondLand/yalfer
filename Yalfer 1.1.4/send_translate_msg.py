from cogs.APIs.google_translate import GoogleTranslateCogFunctionality

def get_tr(text, lang):
    return (GoogleTranslateCogFunctionality.get_translated_text(text, "en", lang))

def get_language(guild, cursor):
    cursor.execute(
        "SELECT * FROM language WHERE guild_id = ?",
        (
            guild.id,
        )
    )
    result = cursor.fetchone()
    if result is None:
        return "en"
    else:
        return result[1]