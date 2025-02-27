import os
import json
import time
from utils.ner_functions import process_ner
from utils.common_functions import beautify_json
from utils.format_functions import compute_and_segment
from utils.srt_functions import json_to_srt_derush

# DERUSH process - dev
# This program is used for testing the script in dev mode 
# --> you can comment all the process and uncomment the one you want to test separately
# --> you can save and analyze the result in 3 JSON outputs


debug_mode = True # Debug mode setting
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_output_stt.json')
OUTPUT_NER_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_output_ner.json')
OUTPUT_FORMAT_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_output_derush.json')
CURRENT_SRC_LANG_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_current_src_lang.txt')


# # ↓
# READ current source language
with open(CURRENT_SRC_LANG_PATH, "r", encoding="utf-8") as lang_file:
    src_lang = lang_file.read().strip()
str_path = os.path.join(os.path.dirname(__file__), f"tmp_test/test_subtitles_{src_lang}.srt")


# ↓
# READ STT
start_time = time.time()
with open(OUTPUT_STT_PATH, "r", encoding="utf-8") as o_stt:
    json_data = json.load(o_stt)
print(f"\n⏰ READ STT process took {time.time() - start_time:.2f} seconds")


# ↓
# NER
start_time = time.time()
ner_result = process_ner(json_data)
print("\nNER results:\n")
print(ner_result)

with open(OUTPUT_NER_PATH, "w", encoding="utf-8") as json_file:
    json.dump(ner_result, json_file, ensure_ascii=False, indent=4)

beautify_json(OUTPUT_NER_PATH, OUTPUT_NER_PATH)
print(f"\n⏰ NER process took {time.time() - start_time:.2f} seconds")
print(f"📥 JSON output NER json compact and saved in {OUTPUT_NER_PATH}")


# ↓
# FORMAT
start_time = time.time()
with open(OUTPUT_NER_PATH, "r", encoding="utf-8") as o_ner:
    json_data = json.load(o_ner)

final_format = compute_and_segment(json_data, debug_mode)
print("\nFORMAT results:\n")
print(final_format)

with open(OUTPUT_FORMAT_PATH, "w", encoding="utf-8") as json_file:
    json.dump(final_format, json_file, ensure_ascii=False, indent=4)

beautify_json(OUTPUT_FORMAT_PATH, OUTPUT_FORMAT_PATH)
print(f"\n⏰ FORMAT process took {time.time() - start_time:.2f} seconds")
print(f"📥 JSON output FORMAT json saved in {OUTPUT_FORMAT_PATH}")


# ↓
# SRT
start_time = time.time()
with open(OUTPUT_FORMAT_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

subtitles = json_to_srt_derush(json_data)
with open(str_path, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\n⏰ SRT process took {time.time() - start_time:.2f} seconds")
print(f"📥 SRT output saved in {str_path}")




