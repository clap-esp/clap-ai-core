# import json
# import sys
# import os

# def find_noise_label(time_start, time_end, pann_events):
#     for event in pann_events:
#         label = event["label"]
#         if label.lower() != "speech":
#             overlap_start = max(time_start, event["time_start"])
#             overlap_end = min(time_end, event["time_end"])
#             if overlap_start < overlap_end:
#                 return label
#     return None

# def merge_stt_and_pann(stt_path, pann_path, output_path):
#     # Charger les fichiers JSON
#     with open(stt_path, "r", encoding="utf-8") as f:
#         stt_data = json.load(f)

#     with open(pann_path, "r", encoding="utf-8") as f:
#         pann_data = json.load(f)

#     # Fusionner les données
#     for entry in stt_data:
#         if entry["text"].strip() == '""""':
#             label = find_noise_label(entry["time_start"], entry["time_end"], pann_data)
#             if label:
#                 entry["text"] = f"[BRUIT] : {label}"
#             else:
#                 entry["text"] = "[BRUIT]"

#     # Sauvegarder le fichier fusionné
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(stt_data, f, indent=4, ensure_ascii=False)

#     print(f"✅ Fichier fusionné sauvegardé : {output_path}")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("❌ Utilisation : python merge_stt_pann.py <stt_json_path> <pann_json_path> <output_json_path>")
#         sys.exit(1)

#     stt_path = sys.argv[1]
#     pann_path = sys.argv[2]
#     output_path = sys.argv[3]

#     if not os.path.exists(stt_path):
#         print(f"❌ Le fichier STT n'existe pas : {stt_path}")
#         sys.exit(1)

#     if not os.path.exists(pann_path):
#         print(f"❌ Le fichier PANN n'existe pas : {pann_path}")
#         sys.exit(1)

#     merge_stt_and_pann(stt_path, pann_path, output_path)


import json
import os
import sys


def find_noise_label(time_start, time_end, pann_events):
    for event in pann_events:
        label = event["label"]
        if label.lower() != "speech":
            overlap_start = max(time_start, event["time_start"])
            overlap_end = min(time_end, event["time_end"])
            if overlap_start < overlap_end:
                return label
    return None

def merge_stt_and_pann(stt_path, pann_path, output_path=None):
    """
    Fusionne les résultats STT avec les détections PANN.

    :param stt_path: Chemin du fichier JSON STT (transcription)
    :param pann_path: Chemin du fichier JSON PANN (bruits détectés)
    :param output_path: Chemin de sortie pour sauvegarder le JSON fusionné (optionnel)
    :return: Chemin du fichier sauvegardé
    """

    if not os.path.exists(stt_path):
        raise FileNotFoundError(f"Le fichier STT n'existe pas : {stt_path}")

    if not os.path.exists(pann_path):
        raise FileNotFoundError(f"Le fichier PANN n'existe pas : {pann_path}")

    with open(stt_path, "r", encoding="utf-8") as f:
        stt_data = json.load(f)

    with open(pann_path, "r", encoding="utf-8") as f:
        pann_data = json.load(f)

    for entry in stt_data:
        if entry["text"].strip() == "":
            label = find_noise_label(entry["time_start"], entry["time_end"], pann_data)
            if label:
                entry["text"] = f"[BRUIT] : {label}"
            # else:
            #     entry["text"] = "[BRUIT]"

    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(os.path.abspath(stt_path)),
            "app_output_stt_merged.json"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stt_data, f, indent=4, ensure_ascii=False)

    print(f"✅ STT fusionné avec PANN sauvegardé : {output_path}")
    return output_path


if __name__ == "__main__":

    stt_path = './API/tmp/app_output_stt.json'
    pann_path = './API/tmp/app_output_pann.json'
    output_path = './API/tmp/app_output_stt_merged.json'

    merge_stt_and_pann(stt_path, pann_path, output_path)
