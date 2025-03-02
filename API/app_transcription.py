import os
import sys
import json
import torch

from pathlib import Path

from transformers import WhisperForConditionalGeneration, AutoProcessor

from utils.audio_extractor import extract_audio_from_video
from utils.stt_functions import process_stt_deprecated, process_stt
from utils.srt_functions import json_to_srt_transcription


# # TRANSCRIPTION process - app
# # This program is used for transcription
#
# debug_mode = False # Debug mode setting
# audio_path_wav = os.path.join(os.path.dirname(__file__), 'audio_before_derush', 'audio_extrait.wav')
# OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'app_stt_output.json')
#
#
# # ↓
# # EXTRACT WAV process
# video_path = ""
# # example usage
# video_path = os.path.join(os.path.dirname(__file__), '..', 'video', 'product_management.mp4')
#
# # this function needs a video path as input
# extract_audio_from_video(video_path)
#
# # ↓
# # STT
# stt_result = process_stt_deprecated(audio_path_wav) # replace with process_stt
#
# # ↓
# # LANG
# # here, we will create a function to detect the language
# lang = "fr"
# str_path = os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{lang}.srt')
#
# # ↓
# # SRT
# subtitles = json_to_srt_transcription(stt_result)
# with open(str_path, "w", encoding="utf-8") as f:
#     f.write(subtitles)
# print(f"\nSRT output saved in {str_path}")
#
# # ↓
# # Save STT output in JSON
# with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
#     json.dump(stt_result, json_file, ensure_ascii=False, indent=4)
# print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")

if __name__ == '__main__':

    if len(sys.argv) > 2:
        video_path: str = sys.argv[1]
        lang: str = sys.argv[2]
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Error: Please check '{video_path}' path.")
    else:
        raise ValueError("Missing video file path or video source language. Usage: python API/app_transcription.py <video_path> <language>")

    str_path = os.path.join(os.path.dirname(__file__), 'exports', f'app_subtitles_{lang}.srt')
    OUTPUT_STT_PATH = os.path.join(os.path.dirname(__file__), 'app_stt_output.json')

    # STT Dependencies
    model_id = "openai/whisper-base"
    whisper_save_dir: str = str((Path.cwd().parent / "models/whisper-base").resolve())  # Change to whisper save dir

    whisper_processor = AutoProcessor.from_pretrained(f"{whisper_save_dir}/processor")
    whisper_model = WhisperForConditionalGeneration.from_pretrained(f"{whisper_save_dir}/model")

    device = torch.device("cpu")
    whisper_model.to(device)
    whisper_model.generation_config.forced_decoder_ids = None

    transcription = process_stt(
        video_path=video_path,
        model=whisper_model,
        processor=whisper_processor,
        source_lang=lang,
    )


    subtitles = json_to_srt_transcription(transcription)
    with open(str_path, "w", encoding="utf-8") as f:
        f.write(subtitles)
    print(f"\nSRT output saved in {str_path}")

    # ↓
    # Save STT output in JSON
    with open(OUTPUT_STT_PATH, 'w', encoding='utf-8') as json_file:
        json.dump(transcription, json_file, ensure_ascii=False, indent=4)
    print(f"\nJSON output STT saved in {OUTPUT_STT_PATH}")

