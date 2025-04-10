import torch
import librosa
import numpy as np
import json
import os
from panns_inference import AudioTagging, labels
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path: str, audio_path: str):
    """
    Extrait l'audio d'un fichier vidéo et le sauvegarde dans un fichier audio.

    Args:
    - video_path (str): Le chemin du fichier vidéo à traiter.
    - audio_path (str): Le chemin où l'audio extrait sera sauvegardé.
    """
    try:
        # Charger la vidéo avec moviepy
        video = VideoFileClip(video_path)
        # Extraire l'audio
        audio = video.audio
        # Sauvegarder l'audio dans un fichier WAV
        audio.write_audiofile(audio_path, codec='pcm_s16le')
        print(f"Audio extrait et sauvegardé dans {audio_path}")
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'audio : {e}")
        raise

def detect_audio_events(audio_path: str, output_path: str, threshold: float = 0.5):
    """
    Détecte des événements sonores dans un fichier audio et enregistre les résultats dans un fichier JSON.

    Args:
    - audio_path (str): Le chemin du fichier audio à analyser.
    - output_path (str): Le chemin du fichier JSON où les résultats seront sauvegardés.
    - threshold (float): Le seuil de détection pour considérer un événement sonore.
    """
    # Charger le modèle
    at = AudioTagging(checkpoint_path=None, device="cuda" if torch.cuda.is_available() else "cpu")

    # Charger l'audio
    audio, sr = librosa.load(audio_path, sr=32000, mono=True)
    audio = np.expand_dims(audio, axis=0)  # Ajoute une dimension pour correspondre au format attendu

    # Définition des paramètres
    segment_length = 10 * 32000  # 10 secondes
    subsegment_length = 1 * 32000  # 1 seconde
    num_segments = audio.shape[-1] // segment_length

    detections = []
    current_detection = None  # Stocke une détection en cours

    for i in range(num_segments):
        start = i * segment_length
        end = start + segment_length
        segment = audio[:, start:end]

        num_subsegments = segment_length // subsegment_length
        for j in range(num_subsegments):
            sub_start = j * subsegment_length
            sub_end = sub_start + subsegment_length
            sub_segment = segment[:, sub_start:sub_end]

            # Conversion pour compatibilité avec le modèle
            sub_segment = torch.tensor(sub_segment).float()

            with torch.no_grad():
                clipwise_output, _ = at.inference(sub_segment.numpy())

            clipwise_output = np.array(clipwise_output).flatten()
            if len(clipwise_output) == 0 or len(clipwise_output) != len(labels):
                continue

            # Identification du son dominant
            best_idx = np.argmax(clipwise_output)
            best_label = labels[best_idx]
            best_score = clipwise_output[best_idx]

            # Calcul des timestamps
            time_start = (i * segment_length + j * subsegment_length) / 32000
            time_end = time_start + 1  # Sous-segments de 1 seconde

            if best_score > threshold:
                # Fusionner les détections similaires
                if current_detection and current_detection["label"] == best_label:
                    current_detection["time_end"] = time_end  # Étend la durée
                else:
                    if current_detection:
                        detections.append(current_detection)  # Sauvegarder la précédente
                    current_detection = {
                        "label": best_label,
                        "time_start": time_start,
                        "time_end": time_end,
                        "confidence": float(best_score)
                    }

    # Sauvegarder la dernière détection en cours
    if current_detection:
        detections.append(current_detection)

    # Exporter en JSON
    with open(output_path, "w") as f:
        json.dump(detections, f, indent=4)

    print(f"Résultats enregistrés dans {output_path}")

if __name__ == "__main__":
    # Exemple de chemins pour un fichier vidéo et un fichier de sortie JSON
    video_path = "../PANN/youtube.mp4"  # Remplacez par votre chemin vidéo
    audio_path = "./API/tmp/extracted_audio.wav"  # Le fichier audio extrait
    output_path = "./API/tmp/app_output_pann.json"  # Le fichier de sortie pour les résultats

    # Extraire l'audio de la vidéo
    extract_audio_from_video(video_path, audio_path)

    # Analyser l'audio extrait
    detect_audio_events(audio_path, output_path)
