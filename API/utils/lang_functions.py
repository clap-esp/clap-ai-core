import os
import json
from langdetect import detect
from utils.lang_map import get_m2m100_code
from utils.srt_functions import json_to_srt_transcription 
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

debug_mode = True
def log(message):
    if debug_mode:
        print(message)


def translate_to_srt(input_path, output_path, src_lang, dest_lang, max_length=128):
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
    tokenizer = M2M100Tokenizer.from_pretrained("./models/m2m100_418M")
    model = M2M100ForConditionalGeneration.from_pretrained("./models/m2m100_418M")
    model.to("cpu")
    
    # Configuring source and target languages ​​in the tokenizer
    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = dest_lang
    
    # Retrieve the ID of the forced token corresponding to the target language
    forced_bos_token_id = tokenizer.get_lang_id(dest_lang)

    with open(input_path, 'r', encoding='utf-8') as file:
        json_input = json.load(file)

    # Extraction of texts to translate
    texts_to_translate = [entry["text"] for entry in json_input]
    log(f"\n---> texts_to_translate")
    log(texts_to_translate)

    # Preparing inputs for translation
    inputs = tokenizer(texts_to_translate, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to("cpu")
    outputs = model.generate(**inputs, max_length=max_length, forced_bos_token_id=forced_bos_token_id)

    # Decoding of translated texts
    translated_texts = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
    log(f"\n---> Translated_texts")
    log(translated_texts)

    # Reintegration of translated texts into the original JSON
    translation_index = 0
    for entry in json_input:
        entry["text"] = translated_texts[translation_index]
        translation_index += 1
    log(f"\n---> json_input")
    log(json_input)

    # Converting translated JSON to SRT format using the json_to_srt_transcription function
    srt_result = json_to_srt_transcription(json_input)
    
    # Saving SRT result to output file
    with open(output_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_result)
    
    print(f"\nThe SRT file was saved as: {output_path}")



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