import deepl
import os
from dotenv import load_dotenv

load_dotenv()
tkey = os.getenv('Translatekey')

def translate(text):
    translator = deepl.Translator(tkey)
    translated = translator.translate_text(text, target_lang="KO")
    return translated