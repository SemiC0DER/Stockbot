import deepl
import os
from dotenv import load_dotenv

load_dotenv()
tkey = os.getenv('Translatekey')

def translate(text):
    translator = deepl.Translator(os.getenv('TRANSLATEKEY'))
    translated = translator.translate_text(text, target_lang="KO")
    return translated