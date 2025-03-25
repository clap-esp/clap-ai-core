import os
import json
from pathlib import Path
from langdetect import detect
from utils.lang_map import get_m2m100_code
from utils.srt_functions import json_to_srt_transcription 
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

debug_mode = True
def log(message):
    if debug_mode:
        print(message)


def translate_str_and_json(input_path, srt_output_path, json_output_path, src_lang, dest_lang, max_length=128):
    print("\nProcessing Traduction in progress...\n")

    mapped_src_lang = get_m2m100_code(src_lang)
    if mapped_src_lang is None:
        print(f"Error: source language {src_lang} is not supported")
        exit(1)
    src_lang = mapped_src_lang

    # Conversion of destination language to M2M100 code
    mapped_dest_lang = get_m2m100_code(dest_lang)
    if mapped_dest_lang is None:
        print(f"Error: destination language {dest_lang} is not supported")
        exit(1)
    dest_lang = mapped_dest_lang

    # Loading tokenizer and model
    base_model_path = Path(__file__).resolve().parent.parent / "models" / "m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(base_model_path)
    model = M2M100ForConditionalGeneration.from_pretrained(base_model_path)
    model.to("cpu")
    
    # Configuring source and target languages ​​in the tokenizer
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = dest_lang
    
    # Retrieve the ID of the forced token corresponding to the target language
    forced_bos_token_id = tokenizer.get_lang_id(dest_lang)

    with open(input_path, 'r', encoding='utf-8') as file:
        json_input = json.load(file)

    # Extract texts to translate
    texts_to_translate = [entry["text"] for entry in json_input]

    CHUNK_SIZE = 200  # maximum lines per batch
    translated_texts = []

    for i in range(0, len(texts_to_translate), CHUNK_SIZE):
        chunk_texts = texts_to_translate[i : i + CHUNK_SIZE]

        # Prepare inputs for translation
        inputs = tokenizer(chunk_texts, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to("cpu")

        # Perform translation on the chunk
        outputs = model.generate(**inputs,max_length=max_length,forced_bos_token_id=forced_bos_token_id)

        # Decode and accumulate results
        chunk_translated = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
        translated_texts.extend(chunk_translated)

    # Reintegrate translated texts into the original JSON
    for entry, translated_line in zip(json_input, translated_texts):
        entry["text"] = translated_line

    # Convert translated JSON to SRT format
    srt_result = json_to_srt_transcription(json_input)
    
    # Save SRT result
    with open(srt_output_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_result)
    print(f"\nSRT output file saved in {srt_output_path}")

    # Save JSON result
    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_input, json_file, ensure_ascii=False, indent=4)
    print(f"\nJSON output file saved in {json_output_path}")



def detect_lang(input_path):
    """
    Detects the language  using `langdetect` of text in the output STT JSON file
    Reads the file and extracts the first 15 non-empty text entries
    Returns str: language code (e.g., "en", "fr") or "unknown" if insufficient text
    """
    print("\nDetecting language...")
    if not os.path.isfile(input_path):
        print(f"The file {input_path} does not exist.")
        exit(1)
    else:
        # Check if the file is empty
        if os.path.getsize(input_path) == 0:
            print(f"The file {input_path} is empty. Please regenerate the transcription")
            exit(1)
    
    with open(input_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    first_ten_texts = [item["text"] for item in json_data[:15] if item["text"].strip()]

    if first_ten_texts:
        combined_text = " ".join(first_ten_texts)
        lang_detected = detect(combined_text)
        lang = lang_detected
        print(f"💬 Detected language: {lang}")
    else:
        lang = "unknown"
        print("Not enough text to detect the language")

    return lang