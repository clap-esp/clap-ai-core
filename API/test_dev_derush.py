import os
import json
from utils.ner_functions import process_ner
from utils.common_functions import beautify_json
from utils.format_functions import compute_and_segment
from utils.srt_functions import json_to_srt_derush

# DERUSH process - dev
# This program is used for testing the script in dev mode 
# --> you can comment all the process and uncomment the one you want to test separately
# --> you can save and analyze the result in 3 JSON outputs


debug_mode = True # Debug mode setting
audio_path_wav = os.path.join(os.path.dirname(__file__), 'audio_before_derush', 'audio_extrait.wav')
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'test_output_stt.json')
OUTPUT_NER_PATH = os.path.join(os.path.dirname(__file__), 'test_output_ner.json')
OUTPUT_FORMAT_PATH = os.path.join(os.path.dirname(__file__), 'test_output_derush.json')
str_path = os.path.join(os.path.dirname(__file__), 'test_subtitles_fr.srt') # fr will be replaced by a parameter in the future


# ↓
# READ STT
with open(OUTPUT_STT_PATH, 'r', encoding='utf-8') as o_stt:
    json_data = json.load(o_stt)
    
# ↓
# NER
ner_result = process_ner(json_data)
print("\nNER results:\n")
print(ner_result)

with open(OUTPUT_NER_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(ner_result, json_file, ensure_ascii=False, indent=4)

beautify_json(OUTPUT_NER_PATH, OUTPUT_NER_PATH)
print(f"\nJSON output NER json compact and saved in {OUTPUT_NER_PATH}")


# ↓
# FORMAT
with open(OUTPUT_NER_PATH, 'r', encoding='utf-8') as o_ner:
    json_data = json.load(o_ner)

final_format = compute_and_segment(json_data)
print("\nFORMAT results:\n")
print(final_format)

with open(OUTPUT_FORMAT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(final_format , json_file, ensure_ascii=False, indent=4)

beautify_json(OUTPUT_FORMAT_PATH, OUTPUT_FORMAT_PATH)
print(f"\nJSON output FORMAT json saved in {OUTPUT_FORMAT_PATH}")


# ↓
# SRT
with open(OUTPUT_FORMAT_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

subtitles = json_to_srt_derush(json_data)
with open(str_path, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\nSRT output saved in {str_path}")