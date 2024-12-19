import os
import json
from utils.stt_functions import process_stt_deprecated # replace with process_stt
from utils.ner_functions import process_ner
from utils.common_functions import beautify_json
from utils.format_functions import compute_and_segment
from utils.srt_functions import json_to_srt_derush


# DERUSH process - app
# This program is used for derushing a video file


debug_mode = False # Debug mode setting
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'app_stt_output.json')
FORMAT_PATH = os.path.join(os.path.dirname(__file__), 'exports', 'app_derush.json')
str_path = os.path.join(os.path.dirname(__file__), 'exports', 'app_subtitles.srt')


# ↓
# READ STT
with open(OUTPUT_STT_PATH, 'r', encoding='utf-8') as o_stt:
    stt_results = json.load(o_stt)

# ↓
# NER
ner_results = process_ner(stt_results)
print("\nNER results:\n")
print(ner_results)

# ↓
# FORMAT
final_format = compute_and_segment(ner_results)
print("\nFormat results:\n")
print(final_format)

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
