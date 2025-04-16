import os
import sys
import time
import json
from utils.lang_functions import detect_lang
from utils.stt_functions import process_stt
from utils.srt_functions import json_to_srt_transcription
from utils.detect_audio_events import extract_audio_from_video, detect_audio_events
from utils.merge_stt_pann import merge_stt_and_pann

# TRANSCRIPTION process - app
# This program is used for transcription

# How to run the script with a video file path and source lang arguments in you console :
#   python API/app_transcription.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4" en
#   python API/app_transcription.py "./video/product_management.mp4" fr
#   python API/app_transcription.py "~/Julie_Ng--Rain_rain_and_more_rain.mp4" en

debug_mode = False # Debug mode setting
OUTPUT_STT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_stt.json'))
CURRENT_SRC_LANG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_current_src_lang.txt'))
OUTPUT_PANN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_pann.json'))
AUDIO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'extracted_audio.wav'))
MERGED_OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_stt_merged.json'))



start_time = time.time()

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
stt_result = process_stt(video_path, source_lang=lang)

# ↓
# Save STT output in JSON
with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")

# ↓
# PANN PROCESS
extract_audio_from_video(video_path, AUDIO_PATH)
detect_audio_events(AUDIO_PATH, OUTPUT_PANN_PATH, threshold=0.5)
# os.system(f"python detect_audio_events.py {video_path} {OUTPUT_PANN_PATH}")

# ↓
# Merge STT and PANN JSON outputs
merge_stt_and_pann(OUTPUT_STT_PATH, OUTPUT_PANN_PATH, MERGED_OUTPUT_PATH)

# ↓
# AUTO DETECT LANG SOURCE
src_lang = detect_lang(MERGED_OUTPUT_PATH)
str_path_srt = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{src_lang}.srt'))
str_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{src_lang}.json'))

# ↓
# SRT + JSON
subtitles = json_to_srt_transcription(stt_result)

with open(str_path_srt, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\nSRT output saved in {str_path_srt}")

with open(str_path_json, "w", encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\nJSON output saved in {str_path_json}")


# ↓
# SAVE DETECTED LANG SOURCE
with open(CURRENT_SRC_LANG_PATH, 'w', encoding='utf-8') as text_file:
    text_file.write(src_lang)
print(f"\nCurrent source language '{src_lang}' saved in text file {CURRENT_SRC_LANG_PATH}")


print(f"\nTRANSCRIPTION SCRIPT process took {int((time.time() - start_time) // 60)} minutes and {int((time.time() - start_time) % 60)} seconds")
