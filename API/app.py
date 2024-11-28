import os
import json
# from fastapi import FastAPI, UploadFile, File, HTTPException
# import uvicorn
from utils.stt_functions import process_stt_deprecated # replace with process_stt
from utils.ner_functions import process_ner
from utils.common_functions import beautify_json
from utils.final_format import compute_and_segment

# This is THE AI-CORE API
# --> but for now it's just a SCRIPT


debug_mode = False # Debug mode setting
audio_path_wav = os.path.join(os.path.dirname(__file__), 'test', 'rush', 'audio_extrait.wav')
FORMAT_PATH = os.path.join(os.path.dirname(__file__), 'final_format.json')


# STT
stt_results = process_stt_deprecated(audio_path_wav) # replace with process_stt

# NER
ner_results = process_ner(stt_results)
print("\nNER results:\n")
print(ner_results)

# FORMAT
final_format = compute_and_segment(ner_results)
print("\nFormat results:\n")
print(final_format)

with open(FORMAT_PATH, 'w', encoding='utf-8') as json_file:
    json.dump(final_format, json_file, ensure_ascii=False, indent=4)

beautify_json(FORMAT_PATH, FORMAT_PATH)
print(f"\nJSON output format json saved in {FORMAT_PATH}")



######################################################
# API ?
# app = FastAPI()
# # Route pour /api/translate
# @app.post("/api/translate")
# async def translate(file: UploadFile = File(...)):
#     try:
#         temp_video_path = f"temp_{file.filename}" 
#         with open(temp_video_path, "wb") as buffer:
#             buffer.write(await file.read())

#         text_output = speech_to_text_function(temp_video_path)
#         os.remove(temp_video_path) 

#         return {"text": text_output}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Route pour /api/derush
# @app.post("/api/derush")
# async def derush(file: UploadFile = File(...)):
#     try:
#         temp_video_path = f"temp_{file.filename}"
#         with open(temp_video_path, "wb") as buffer:
#             buffer.write(await file.read())

#         text_output = speech_to_text_function(temp_video_path)

#         ner_output = ner_function(text_output)

#         os.remove(temp_video_path)

#         return {"entities": ner_output}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="127.0.0.1", port=8000)
