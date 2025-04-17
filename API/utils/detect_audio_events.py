import torch
import librosa
import numpy as np
import json
import os
from panns_inference import AudioTagging, labels
from moviepy.editor import VideoFileClip

MODEL_DIR = "./API/models"
MODEL_PATH = os.path.join(MODEL_DIR, "Cnn14_16k_mAP=0.438.pth")

def download_model_if_needed():
    """
    Télécharge et enregistre le modèle localement si ce n'est pas déjà fait.
    """
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        print("Téléchargement du modèle...")
        # On initialise le modèle avec téléchargement
        model = AudioTagging(checkpoint_path=None, device="cpu")  # peu importe l'appareil ici
        # Sauvegarde du modèle
        torch.save(model.model.state_dict(), MODEL_PATH)
        print(f"Modèle téléchargé et sauvegardé dans {MODEL_PATH}")
    else:
        print(f"Modèle déjà présent à {MODEL_PATH}")

def load_audio_tagger():
    """
    Charge le modèle à partir du fichier local.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Chargement du modèle depuis {MODEL_PATH} sur {device}")
    model = AudioTagging(checkpoint_path=None, device=device)
    model.model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    return model

def extract_audio_from_video(video_path: str, audio_path: str):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, codec='pcm_s16le')
        print(f"Audio extrait et sauvegardé dans {audio_path}")
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'audio : {e}")
        raise

def detect_audio_events(audio_path: str, output_path: str, threshold: float = 0.5):
    download_model_if_needed()
    at = load_audio_tagger()

    audio, sr = librosa.load(audio_path, sr=32000, mono=True)
    audio = np.expand_dims(audio, axis=0)

    segment_length = 10 * 32000
    subsegment_length = 1 * 32000
    num_segments = audio.shape[-1] // segment_length

    detections = []
    current_detection = None

    for i in range(num_segments):
        start = i * segment_length
        end = start + segment_length
        segment = audio[:, start:end]

        num_subsegments = segment_length // subsegment_length
        for j in range(num_subsegments):
            sub_start = j * subsegment_length
            sub_end = sub_start + subsegment_length
            sub_segment = segment[:, sub_start:sub_end]

            sub_segment = torch.tensor(sub_segment).float()

            with torch.no_grad():
                clipwise_output, _ = at.inference(sub_segment.numpy())

            clipwise_output = np.array(clipwise_output).flatten()
            if len(clipwise_output) == 0 or len(clipwise_output) != len(labels):
                continue

            best_idx = np.argmax(clipwise_output)
            best_label = labels[best_idx]
            best_score = clipwise_output[best_idx]

            time_start = (i * segment_length + j * subsegment_length) / 32000
            time_end = time_start + 1

            if best_score > threshold:
                if current_detection and current_detection["label"] == best_label:
                    current_detection["time_end"] = time_end
                else:
                    if current_detection:
                        detections.append(current_detection)
                    current_detection = {
                        "label": best_label,
                        "time_start": time_start,
                        "time_end": time_end,
                        "confidence": float(best_score)
                    }

    if current_detection:
        detections.append(current_detection)

    with open(output_path, "w") as f:
        json.dump(detections, f, indent=4)

    print(f"Résultats enregistrés dans {output_path}")

if __name__ == "__main__":
    video_path = "../PANN/youtube.mp4"
    audio_path = "./API/tmp/extracted_audio.wav"
    output_path = "./API/tmp/app_output_pann.json"

    extract_audio_from_video(video_path, audio_path)
    detect_audio_events(audio_path, output_path)
