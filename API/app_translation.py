import os
from utils.lang_functions import translate_srt_file


# TRANSLATION process - app
# This program is used for translate in a specifique langage


# ↓
# TRANSLATE + langue
src_lang="fr"
dest_lang="en"
input_path = os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{src_lang}.srt')
output_path = os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{dest_lang}.srt')

print (f"Translating")
translate_srt_file(input_path, output_path, src_lang, dest_lang)
print(f"\nSRT output saved in {output_path}")

