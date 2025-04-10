# Etude pour la fonction de traduction

## Contexte

L'API gratuite de GoogleTranslator a une execution rapide car les serveurs sont puissant.
Mais il arrive que l'API ait des coupures de service est nous retourne des erreur 500.  
`Translated: Error 500 (Server Error)!!1500.That’s an error.There was an error. Please try again later.That’s all we know.`  
De plus cette solution necessite une connexion internet et l'idéal serait de pouvoir utiliser l'application CLAP hors ligne.
C'est pourquoi cette étude vise à trouver le meilleur modèle pour la fonctionnalité de traduction.

## Comparaison des solutions techniques

Ces solutions ont été testées avec une vidéo de 11 minutes.

Pour les modèles text-to-text appelés en local, l'exécution peut durer plusieurs dizaines de minutes. Pour améliorer les perf, le texte est extrait du json et placé dans un tableau pour qu'il n'y ait qu'un seul appel au modèle au lieu d'un appel à chaque itération. Cela permet d'obtenir des temps d'exécution < 10 min. La convertion json to srt ne prendra derrière qu'une demi-seconde.

| Modèle             | Type           | Tps  | Poid    | Points positifs          | Points négatifs                                 |
| ------------------ | -------------- | ---- | ------- | ------------------------ | ----------------------------------------------- |
| GoogleTranslator   | srt vers srt   | 20'  | API     | Rapide et simple         | Besoin d'internet, coupures de service possible |
| Whisper-base       | Audio vers srt | 550' | 278 Mo  | -                        | Voir notes ci-dessous\*                         |
| nllb-200-distilled | json vers json | 210' | 2,32 Go | Ne traduit pas '[Bruit]' | Laisse des phrases dans la langue source        |
| bloomz-560m        | json vers json | 700' | 2,10 Go | Qualité des trad         | Nécessite un prompt / output difficile à config |
| mbart-large-50     | json vers json | 299' | 2,29 Go | Simple à configurer      | `[Wednesday]` dans la sortie                    |
| m2m100_418M        | json vers json | 178' | 1,80 Go | pas anglais centré       | -                                               |

- Note whisper:
  - Difficulté de configuration pour la traductions d'une langue cible différente que l'anglais (par default)
  - Necessite de configurer les chunk qui seront différent du découpage de d'une traduction à une autre.

## Choix du modèle

Le modèle [m2m100_418M](https://ai.meta.com/blog/introducing-many-to-many-multilingual-machine-translation) de Meta permet la traduction entre de nombreuses paires de langues en un seul système. Il exploite des techniques pour capturer des représentations linguistiques communes et réduire le gap de qualité entre les langues à faibles ressources et langues plus répandues. C'est également le moins gourmand en ressource.

## Pipeline de traduction

Dans le script `app_translation.py`, l'enregistrement de la langue source en cache, permet à l'utilisateur d'effectuer une traduction vers n'importe quelle langue cible. Ce script a seulement besoin qu'on lui passe en paramètre la langue cible car la langue source est detecté automatiquement via la librairie python `langdetect`.

Cette lib supporte 55 langues en format ISO 639-1 codes

```
af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,
hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl,
pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw
```

Pour passer correctement la langue source au modèle, un matching doit être effectuer avec les codes langue de m2m100. Voir le fichier [utils/lang_map.py](../API/utils/lang_map.py)

## Langue disponible

Voici la liste des langues diponible pour l'application CLAP à ce jour.

```json
[
  { "code": "af", "language": "Afrikaans" },
  { "code": "ar", "language": "Arabic" },
  { "code": "bg", "language": "Bulgarian" },
  { "code": "bn", "language": "Bengali" },
  { "code": "ca", "language": "Catalan" },
  { "code": "cs", "language": "Czech" },
  { "code": "cy", "language": "Welsh" },
  { "code": "da", "language": "Danish" },
  { "code": "de", "language": "German" },
  { "code": "el", "language": "Greek" },
  { "code": "en", "language": "English" },
  { "code": "es", "language": "Spanish" },
  { "code": "et", "language": "Estonian" },
  { "code": "fa", "language": "Persian" },
  { "code": "fi", "language": "Finnish" },
  { "code": "fr", "language": "French" },
  { "code": "gu", "language": "Gujarati" },
  { "code": "he", "language": "Hebrew" },
  { "code": "hi", "language": "Hindi" },
  { "code": "hr", "language": "Croatian" },
  { "code": "hu", "language": "Hungarian" },
  { "code": "id", "language": "Indonesian" },
  { "code": "it", "language": "Italian" },
  { "code": "ja", "language": "Japanese" },
  { "code": "kn", "language": "Kannada" },
  { "code": "ko", "language": "Korean" },
  { "code": "lt", "language": "Lithuanian" },
  { "code": "lv", "language": "Latvian" },
  { "code": "mk", "language": "Macedonian" },
  { "code": "ml", "language": "Malayalam" },
  { "code": "mr", "language": "Marathi" },
  { "code": "ne", "language": "Nepali" },
  { "code": "nl", "language": "Dutch" },
  { "code": "no", "language": "Norwegian" },
  { "code": "pa", "language": "Panjabi" },
  { "code": "pl", "language": "Polish" },
  { "code": "pt", "language": "Portuguese" },
  { "code": "ro", "language": "Romanian" },
  { "code": "ru", "language": "Russian" },
  { "code": "sk", "language": "Slovak" },
  { "code": "sl", "language": "Slovenian" },
  { "code": "so", "language": "Somali" },
  { "code": "sq", "language": "Albanian" },
  { "code": "sv", "language": "Swedish" },
  { "code": "sw", "language": "Swahili" },
  { "code": "ta", "language": "Tamil" },
  { "code": "te", "language": "Telugu" },
  { "code": "th", "language": "Thai" },
  { "code": "tl", "language": "Tagalog" },
  { "code": "tr", "language": "Turkish" },
  { "code": "uk", "language": "Ukrainian" },
  { "code": "ur", "language": "Urdu" },
  { "code": "vi", "language": "Vietnamese" },
  { "code": "zh-cn", "language": "Chinese Simplified" }
]
```

## Code déployé pour l'étude

```py
##################
# mbart-large-50 #
##################
import torch
import time
import json
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

def download_mbart50_model_hf(
    model_name: str = "facebook/mbart-large-50-many-to-many-mmt",
    save_dir: str = "./models"
):
    os.makedirs(save_dir, exist_ok=True)
    model_save_path = os.path.join(save_dir, model_name.split('/')[-1])

    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
    model = MBartForConditionalGeneration.from_pretrained(model_name)

    tokenizer.save_pretrained(model_save_path)
    model.save_pretrained(model_save_path)

    print(f"Modèle {model_name} téléchargé et sauvegardé")

def translate_json_file(input_filepath, output_filepath, model_local_path, src_lang="fr_XX", dest_lang="en_XX", max_length=128):
    tokenizer = MBart50TokenizerFast.from_pretrained(model_local_path)
    model = MBartForConditionalGeneration.from_pretrained(model_local_path)
    device = torch.device("cpu")
    model.to(device)

    tokenizer.src_lang = src_lang
    forced_bos_token_id = tokenizer.lang_code_to_id[dest_lang]

    with open(input_filepath, 'r', encoding='utf-8') as file:
        json_input = json.load(file)

    # Extraction des textes à traduire
    texts_to_translate = [entry["text"] for entry in json_input]
    print(texts_to_translate)

    inputs = tokenizer(texts_to_translate, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(device)
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, max_length=max_length)

    # Décodage des textes traduits
    translated_texts = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
    print("\ntranslated_texts")
    print(translated_texts)

    # Réintégration des textes traduits
    translation_index = 0
    for entry in json_input:
        entry["text"] = translated_texts[translation_index]
        translation_index += 1

    # Écriture du JSON output
    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(json_input, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    print("\nTéléchargement du modèle mBART‑50...")
    download_mbart50_model_hf(model_name="facebook/mbart-large-50-many-to-many-mmt",save_dir="./models")
    model_path = "./models/mbart-large-50-many-to-many-mmt"
    print("\nTraduction du fichier JSON...")
    start_time = time.time()
    translate_json_file("input.json", "output.json", model_path, src_lang="fr_XX", dest_lang="en_XX")
    print(f"\n⏰ Le processus de traduction a été complété en {time.time() - start_time:.2f} secondes")


######################
# nllb-200-distilled #
######################
import torch
import time
import json
import os
# from transformers import NllbTokenizer, NllbForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def download_nllb_model_hf(
    model_name: str = "facebook/nllb-200-distilled-600M",
    save_dir: str = "./models"
):
    os.makedirs(save_dir, exist_ok=True)
    model_save_path = os.path.join(save_dir, model_name.split('/')[-1])
    # tokenizer = NllbTokenizer.from_pretrained(model_name)
    # model = NllbForConditionalGeneration.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")

    tokenizer.save_pretrained(model_save_path)
    model.save_pretrained(model_save_path)

    print(f"Modèle {model_name} téléchargé et sauvegardé")

def translate_json_file(input_filepath, output_filepath, model_local_path, src_lang="fr", dest_lang="en", max_length=128):
    # tokenizer = NllbTokenizer.from_pretrained(model_local_path)
    # model = NllbForConditionalGeneration.from_pretrained(model_local_path)
    tokenizer = AutoTokenizer.from_pretrained(model_local_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_local_path)
    device = torch.device("cpu")
    model.to(device)

    # Set the forced_bos_token_id based on destination language code
    # model.config.forced_bos_token_id = tokenizer.lang2id["eng_Latn"] # avec NllbTokenizer
    model.config.forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")

    with open(input_filepath, 'r', encoding='utf-8') as file:
        json_input = json.load(file)

    texts_to_translate = [entry["text"] for entry in json_input]
    print(texts_to_translate)

    # Remove src_lang and tgt_lang arguments here.
    inputs = tokenizer(
        texts_to_translate,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length
    ).to(device)

    outputs = model.generate(**inputs, max_length=max_length)
    translated_texts = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
    print("\ntranslated_texts", translated_texts)


    for translation_index, entry in enumerate(json_input):
        entry["text"] = translated_texts[translation_index]

    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(json_input, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # print("\nTéléchargement du modèle NLLB-200 Distilled...")
    download_nllb_model_hf(model_name="facebook/nllb-200-distilled-600M", save_dir="./models")
    model_path = "./models/nllb-200-distilled-600M"
    print("\nTraduction du fichier JSON...")
    start_time = time.time()
    translate_json_file("input.json", "output.json", model_path, src_lang="fr", dest_lang="en")
    print(f"\n⏰ Le processus de traduction a été complété en {time.time() - start_time:.2f} secondes")


###############
# m2m100_418M #
###############
import time
import json
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

def translate_json_file(input_filepath, output_filepath, model_local_path, src_lang="fr", dest_lang="en", max_length=128):

    tokenizer = M2M100Tokenizer.from_pretrained(model_local_path)
    model = M2M100ForConditionalGeneration.from_pretrained(model_local_path)
    model.to("cpu")

    tokenizer.src_lang = src_lang
    tokenizer.tgt_lang = dest_lang

    # Important : récupérer l'ID du token forcé correspondant à la langue cible
    forced_bos_token_id = tokenizer.get_lang_id(dest_lang)

    with open(input_filepath, 'r', encoding='utf-8') as file:
        json_input = json.load(file)

    # Extraction des textes à traduire
    texts_to_translate = [entry["text"] for entry in json_input]
    print(texts_to_translate)

    inputs = tokenizer(texts_to_translate, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to("cpu")
    outputs = model.generate(**inputs, max_length=max_length, forced_bos_token_id=forced_bos_token_id)

    # Décodage des textes traduits
    translated_texts = [tokenizer.decode(g, skip_special_tokens=True) for g in outputs]
    print("\ntranslated_texts")
    print(translated_texts)

    # Réintégration des textes traduits
    translation_index = 0
    for entry in json_input:
        entry["text"] = translated_texts[translation_index]
        translation_index += 1

    # Écriture du JSON
    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(json_input, file, indent=4, ensure_ascii=False)

# Utilisation de la fonction
if __name__ == "__main__":
    model_path = "./models/m2m100_418M"
    print("\nTraduction du fichier JSON...")
    start_time = time.time()
    translate_json_file("input.json", "output.json", model_path, src_lang="fr", dest_lang="en")
    print(f"\n⏰ Le processus de traduction a été complété en {time.time() - start_time:.2f} secondes")


###############
# bloomz-560m #
###############
import torch
import time
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

def translate_json_file(input_filepath, output_filepath, model_local_path, src_lang="French", dest_lang="English", max_length=512):

    tokenizer = AutoTokenizer.from_pretrained(model_local_path)
    model = AutoModelForCausalLM.from_pretrained(model_local_path)
    model.to("cpu")

    with open(input_filepath, 'r', encoding='utf-8') as file:!!
        json_input = json.load(file)

    texts_to_translate = [entry["text"] for entry in json_input]
    translated_texts = []

    for text in texts_to_translate:
        prompt = f"Translate from {src_lang} to {dest_lang}: {text}"
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to("cpu")
        outputs = model.generate(**inputs, max_length=max_length)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translated_texts.append(translated_text)

    for entry, translation in zip(json_input, translated_texts):
        entry["text"] = translation

    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(json_input, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    model_path = "./models/bloomz-560m"
    print("\nTraduction du fichier JSON...")
    start_time = time.time()
    translate_json_file("input.json", "output.json", model_path)
    print(f"\n⏰ Le processus de traduction a été complété en {time.time() - start_time:.2f} secondes")


###########
# Whisper #
###########
import os
import time
import torch
import torchaudio
import soundfile as sf
from transformers import WhisperForConditionalGeneration, WhisperProcessor

def download_whisper_model_hf(model_name: str = "openai/whisper-base", save_dir: str = "./models"):
    os.makedirs(save_dir, exist_ok=True)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    processor = WhisperProcessor.from_pretrained(model_name)
    local_path = os.path.join(save_dir, model_name.split('/')[-1])
    os.makedirs(local_path, exist_ok=True)
    model.save_pretrained(local_path)
    processor.save_pretrained(local_path)

def seconds_to_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def translate_str_and_json(
    audio_file: str,
    output_file: str,
    model_local_path: str = "./models/whisper-base",
    target_language: str = "en",  # langue cible (par défaut anglais)
    chunk_duration: float = 3.0
):
    model = WhisperForConditionalGeneration.from_pretrained(model_local_path)
    processor = WhisperProcessor.from_pretrained(model_local_path)
    model.eval()
    device = torch.device("cpu")
    model.to(device)

    audio_input, sample_rate = sf.read(audio_file)
    if sample_rate != 16000:
        audio_tensor = torch.tensor(audio_input.T if audio_input.ndim == 2 else audio_input, dtype=torch.float32)
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        audio_tensor = resampler(audio_tensor)
        if audio_tensor.ndim > 1:
            audio_tensor = torch.mean(audio_tensor, dim=0)
        audio_input = audio_tensor.numpy()
        sample_rate = 16000

    total_samples = len(audio_input)
    chunk_size = int(chunk_duration * sample_rate)
    segments = []

    for i in range(0, total_samples, chunk_size):
        segment_audio = audio_input[i:i+chunk_size]
        if len(segment_audio) < chunk_size:
            import numpy as np
            segment_audio = np.pad(segment_audio, (0, chunk_size - len(segment_audio)), mode='constant')

        # Si la langue cible est l'anglais, on utilise la tâche de traduction intégrée
        if target_language.lower() == "en":
            # Utilise la tâche "translate" pour traduire en anglais
            input_features = processor(segment_audio, sampling_rate=sample_rate, return_tensors="pt").input_features.to(device)
            with torch.no_grad():
                predicted_ids = model.generate(input_features, task="translate")
            text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        else:
            # Pour toute autre langue, on fait une simple transcription.
            # Ici, on précise la langue source pour améliorer la transcription.
            input_features = processor(segment_audio, sampling_rate=sample_rate, return_tensors="pt", language="fr").input_features.to(device)
            with torch.no_grad():
                predicted_ids = model.generate(input_features)
            # La transcription sera en français.
            text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            # Pour traduire dans target_language, il faudrait une étape supplémentaire de traduction,
            # ce qui n'est pas directement supporté par Whisper.
            if target_language.lower() != "fr":
                text += f" [Traduction vers {target_language} non réalisée par Whisper]"

        start_time_seg = i / sample_rate
        end_time_seg = min((i + chunk_size) / sample_rate, total_samples / sample_rate)
        segments.append((start_time_seg, end_time_seg, text))

    # Création du fichier SRT
    with open(output_file, "w", encoding="utf-8") as f_out:
        for idx, (start, end, text) in enumerate(segments, start=1):
            f_out.write(f"{idx}\n")
            f_out.write(f"{seconds_to_timestamp(start)} --> {seconds_to_timestamp(end)}\n")
            f_out.write(text + "\n\n")

if __name__ == "__main__":
    print("\nTranscription in progress...")
    start_time = time.time()

    # Téléchargement du modèle Whisper
    # download_whisper_model_hf("openai/whisper-base", save_dir="./models")

    audio_file = "./API/tmp/audio_before_derush/audio_extrait.wav"
    output_file = "transcription.srt"

    translate_str_and_json(
        audio_file=audio_file,
        output_file=output_file,
        model_local_path="./models/whisper-base",
        target_language="es",
        chunk_duration=3.0
    )

    print(f"\n⏰ Transcription process took {time.time() - start_time:.2f} seconds")
    print(f"SRT output saved in {output_file}")

```
