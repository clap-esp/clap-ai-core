import os
import sys
import time
from utils.lang_functions import translate_str_and_json

# TRANSLATION process - app
# This program is used to translate into a target language

# How to run the script with a language code argument:
#   Ex (Spanish): `python API/app_translation.py es`
#   Make sure the language code is supported in `API/utils/map_lang.py`


# ↓
# READ current source language
CURRENT_SRC_LANG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_current_src_lang.txt'))
with open(CURRENT_SRC_LANG_PATH, "r", encoding="utf-8") as lang_file:
    src_lang = lang_file.read().strip()


# ↓ CHECK `dest_lang` -> target language argument
if len(sys.argv) > 1:
    dest_lang = sys.argv[1]
else:
    raise ValueError("Missing target language. Please provide 'dest_lang' as an argument")


# ↓
# TRANSLATE
TEXT_TO_TRANSLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_stt.json'))
SRT_OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports', f"app_subtitles_{dest_lang}.srt"))
JSON_OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports', f"app_subtitles_{dest_lang}.json"))

print(f"🔍 Source language: {src_lang}")
print(f"🏁 Destination language: {dest_lang}")

start_time = time.time()
translate_str_and_json(TEXT_TO_TRANSLATE_PATH, SRT_OUTPUT_PATH, JSON_OUTPUT_PATH, src_lang, dest_lang)

print(f"\n⏰ Translation process took {time.time() - start_time:.2f} seconds")