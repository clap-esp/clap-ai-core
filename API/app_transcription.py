import os
import sys
import json
import time
from utils.audio_extractor import extract_audio_from_video
from utils.stt_functions import process_stt_deprecated # replace with process_stt
from utils.lang_functions import detect_lang
from utils.srt_functions import json_to_srt_transcription


# TRANSCRIPTION process - app
# This program is used for transcription

# How to run the script with a video file full path argument in you console:
#   python API/app_transcription.py "~/Julie_Ng--Rain_rain_and_more_rain.mp4"
#   python API/app_transcription.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4"


debug_mode = False # Debug mode setting
audio_path_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'audio_before_derush', 'audio_extrait.wav'))
OUTPUT_STT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_output_stt.json'))
CURRENT_SRC_LANG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'app_current_src_lang.txt'))

start_time = time.time()


# ↓ CHECK `video_path`
if len(sys.argv) > 1:
    video_path = sys.argv[1]
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: File '{video_path}' not found. Please check the path")
else:
    raise ValueError("Missing video file path. Usage: python API/app_transcription.py <video_path>")


# ↓
# EXTRACT WAV
# this function needs a video path as input
extract_audio_from_video(video_path)

# ↓
# SPEECH-TO-TEXT (STT) PROCESS
stt_result = process_stt_deprecated(audio_path_wav) # replace with process_stt

# ↓
# Save STT output in JSON
with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")

# ↓
# AUTO DETECT LANG SOURCE
src_lang = detect_lang(OUTPUT_STT_PATH)
str_path_srt = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'exports', f'app_subtitles_{src_lang}.srt'))
str_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'exports', f'app_subtitles_{src_lang}.json'))

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