import os
import json
import time
from utils.ner_functions import process_ner
from utils.common_functions import beautify_json
from utils.format_functions import compute_and_segment
from utils.srt_functions import json_to_srt_derush


# DERUSH process - app
# This program is used for derushing a video file


debug_mode = False # Debug mode setting

OUTPUT_STT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_stt.json'))
FORMAT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'exports', 'app_derush.json'))
CURRENT_SRC_LANG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_current_src_lang.txt'))

start_time = time.time()

# ↓
# READ current source language
with open(CURRENT_SRC_LANG_PATH, "r", encoding="utf-8") as lang_file:
    src_lang = lang_file.read().strip()
str_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'exports', f"app_subtitles_{src_lang}.srt"))


# ↓
# READ STT
with open(OUTPUT_STT_PATH, 'r', encoding='utf-8') as o_stt:
    stt_results = json.load(o_stt)

# ↓
# NER
ner_results = process_ner(stt_results)


# ↓
# FORMAT
final_format = compute_and_segment(ner_results, debug_mode)

with open(FORMAT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(final_format, json_file, ensure_ascii=False, indent=4)

beautify_json(FORMAT_PATH, FORMAT_PATH)
print(f"\nJSON output format json saved in {FORMAT_PATH}")

# ↓
# SRT
srt_result = json_to_srt_derush(final_format)
with open(str_path, "w", encoding="utf-8") as f:
    f.write(srt_result)
print(f"\nSRT output saved in {str_path}")


print(f"\n⏰ DERUSH SCRIPT process took {int((time.time() - start_time) // 60)} minutes and {int((time.time() - start_time) % 60)} seconds")