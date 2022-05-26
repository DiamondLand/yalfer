import json
import requests
from googletrans import Translator


class GoogleTranslateCogFunctionality:

    @staticmethod
    def get_translated_text(text, source, dest):
        return Translator().translate(
            text,
            src=source,
            dest=dest).text
