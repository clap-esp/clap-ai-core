import os
import sys
import json
import time
from utils.audio_extractor import extract_audio_from_video
from utils.stt_functions import process_stt_deprecated  # replace with process_stt
from utils.lang_functions import detect_lang
from utils.srt_functions import json_to_srt_transcription


# TRANSCRIPTION process - test
# This program is used for testing the script in dev mode 
# --> you can comment all the process and uncomment the one you want to test separately

# How to run the script with a video file path argument in you console:
#   cd ~/Desktop/CLAP_DEV/clap-ai-core/
#   python API/app_transcription.py " ~/product_management.mp4"
#   python API/app_transcription.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4"


debug_mode = True  # Debug mode setting
audio_path_wav = os.path.join(os.path.dirname(__file__), 'tmp', 'audio_before_derush', 'audio_extrait.wav')
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_output_stt.json')
CURRENT_SRC_LANG_PATH = os.path.join(os.path.dirname(__file__), 'tmp_test', 'test_current_src_lang.txt')


# ↓ CHECK `video_path`
if len(sys.argv) > 1:
    video_path = os.path.abspath(sys.argv[1])  # Convert to absolute path
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: File '{video_path}' not found. Please check the path")
else:
    raise ValueError("Missing video file path. Usage: python API/app_transcription.py <video_path>")


# # ↓
# EXTRACT (WAV) from video
start_time = time.time()
extract_audio_from_video(video_path)
print(f"\n⏰ EXTRACT WAV process took {time.time() - start_time:.2f} seconds")


# ↓
# SPEECH-TO-TEXT (STT) PROCESS
start_time = time.time()
stt_result = process_stt_deprecated(audio_path_wav)  # replace with process_stt
print(f"\n⏰ STT process took {time.time() - start_time:.2f} seconds")

with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"📥 JSON output STT saved in {OUTPUT_STT_PATH}")


# ↓
# AUTO DETECT LANG SOURCE
start_time = time.time()
src_lang = detect_lang(OUTPUT_STT_PATH)
str_path = os.path.join(os.path.dirname(__file__), f'tmp_test/test_subtitles_{src_lang}.srt')
print(f"srt_path: {str_path}")
print(f"\n⏰ AUTO DETECT LANG process took {time.time() - start_time:.2f} seconds")


# ↓
# SRT
start_time = time.time()
with open(OUTPUT_STT_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

subtitles = json_to_srt_transcription(json_data)
with open(str_path, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\n⏰ SRT process took {time.time() - start_time:.2f} seconds")
print(f"📥 SRT output saved in {str_path}")


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

