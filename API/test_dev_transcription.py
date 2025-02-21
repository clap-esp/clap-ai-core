import os
import json
from utils.audio_extractor import extract_audio_from_video
from utils.stt_functions import process_stt_deprecated # replace with process_stt
from utils.srt_functions import json_to_srt_transcription


# TRANSCRIPTION process
# This program is used for for testing the script in dev mode 
# --> you can comment all the process and uncomment the one you want to test separately


debug_mode = False # Debug mode setting
audio_path_wav = os.path.join(os.path.dirname(__file__), 'audio_before_derush', 'audio_extrait.wav')
OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'test_output_stt.json')


# ↓
# EXTRACT WAV process
video_path = ""
# example usage
video_path = os.path.join(os.path.dirname(__file__), '..', 'video', 'product_management.mp4')

# this function needs a video path as input
extract_audio_from_video(video_path)

# ↓
# STT
stt_result = process_stt_deprecated(audio_path_wav) # replace with process_stt

with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")


# ↓
# LANG
# detect language
lang = "fr"
str_path = os.path.join(os.path.dirname(__file__), f'test_subtitles_{lang}.srt')


# ↓
# SRT
with open(OUTPUT_STT_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

subtitles = json_to_srt_transcription(json_data)
with open(str_path, "w", encoding="utf-8") as f:
    f.write(subtitles)
print(f"\nSRT output saved in {str_path}")


# ↓
# Save STT output in JSON
with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")