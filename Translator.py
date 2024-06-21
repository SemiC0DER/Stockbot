import deepl
import os

key_path = os.path.dirname( os.path.abspath( __file__ ) )+"/translatekey.txt"
t = open(key_path,"r",encoding="utf-8")
tkey = t.read().split()[0]

def translate(text):
    translator = deepl.Translator(tkey)
    translated = translator.translate_text(text, target_lang="KO")
    return translated