import os
import sys
import json
import time
import torch
from utils.lang_functions import detect_lang
from utils.stt_functions import process_stt
from utils.srt_functions import json_to_srt_transcription
from pathlib import Path
from transformers import WhisperForConditionalGeneration, AutoProcessor


# TRANSCRIPTION process - test
# This program is used for testing the script in dev mode 
# --> you can comment all the process and uncomment the one you want to test separately

# How to run the script with a video file path and source lang arguments in you console :
#   cd ~/Desktop/CLAP_DEV/clap-ai-core/
#   python API/test_dev_transcription.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4" en
#   python API/test_dev_transcription.py "~/Julie_Ng--Rain_rain_and_more_rain.mp4" en


debug_mode = True  # Debug mode setting
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_output_stt.json')
CURRENT_SRC_LANG_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_current_src_lang.txt')


# ↓ CHECK `video_path` and `lang`
if len(sys.argv) > 2:
    video_path: str = sys.argv[1]
    lang: str = sys.argv[2]
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: Please check '{video_path}' path.")
else:
    raise ValueError("Missing video file path or source language. Usage: python API/app_transcription.py <video_path> <language>")


# ↓
# SPEECH-TO-TEXT (STT) PROCESS
start_time = time.time()
stt_result = process_stt(video_path, source_lang=lang)
with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"📥 JSON output STT saved in {OUTPUT_STT_PATH}")
print(f"\n⏰ SPEECH-TO-TEXT process took {time.time() - start_time:.2f} seconds")


# ↓
# AUTO DETECT LANG SOURCE
start_time = time.time()
src_lang = detect_lang(OUTPUT_STT_PATH)
str_path_srt = os.path.join(os.path.dirname(__file__), f'tmp_test/test_subtitles_{src_lang}.srt')
str_path_json = os.path.join(os.path.dirname(__file__), f'tmp_test/test_subtitles_{src_lang}.json')
print(f"srt_path: {str_path_srt}")
print(f"\n⏰ AUTO DETECT LANG process took {time.time() - start_time:.2f} seconds")


# ↓
# SRT + JSON
start_time = time.time()
with open(OUTPUT_STT_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

with open(str_path_json, "w", encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

subtitles = json_to_srt_transcription(json_data)
with open(str_path_srt, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\n⏰ SRT + JON process took {time.time() - start_time:.2f} seconds")
print(f"\n📥 JSON output saved in {str_path_json}")
print(f"📥 SRT output saved in {str_path_srt}")


# ↓
# Save STT output in JSON
start_time = time.time()
with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\n⏰ Save STT output in JSON process took {time.time() - start_time:.2f} seconds")
print(f"📥 JSON output STT saved in {OUTPUT_STT_PATH}")


# ↓
# SAVE DETECTED LANG SOURCE
start_time = time.time()
with open(CURRENT_SRC_LANG_PATH, 'w', encoding='utf-8') as text_file:
    text_file.write(src_lang)
print(f"\n⏰ Save Current Source Language in text file took {time.time() - start_time:.2f} seconds")
print(f"📥 Text file Current source language '{src_lang}' saved in {CURRENT_SRC_LANG_PATH}")

