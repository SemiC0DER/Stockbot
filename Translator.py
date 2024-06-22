import deepl
import os

def translate(text):
    translator = deepl.Translator(os.getenv('TRANSLATEKEY'))
    translated = translator.translate_text(text, target_lang="KO")
    return translated