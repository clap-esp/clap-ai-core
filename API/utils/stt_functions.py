import torch
from pathlib import Path
from transformers import WhisperForConditionalGeneration, WhisperProcessor

from .speech_to_text import STTTranscriber
from .audio_extractor import extract_audio_features


debug_mode = None
def log(message):
    if debug_mode:
        print(message)


def initialize_whisper():
    """Initialise and retourn Whisper"""
    try:
        base_model_path = Path(__file__).resolve().parent.parent / "models" / "whisper-base"
        processor_path = base_model_path / "processor"
        model_path = base_model_path / "model"

        whisper_processor = WhisperProcessor.from_pretrained(processor_path)
        whisper_model = WhisperForConditionalGeneration.from_pretrained(model_path)

        device = torch.device("cpu")
        whisper_model.to(device)
        whisper_model.generation_config.forced_decoder_ids = None
        
        return whisper_model, whisper_processor
    except Exception as e:
        log(f"Failed to initialize Whisper model: {e}")
        raise

def process_stt(video_path: str, source_lang: str):
    model, processor = initialize_whisper()
    transcriber = STTTranscriber(model=model, processor=processor)

    audio_segments = extract_audio_features(video_path, use_effect_split=True)
    transcriber.process_audio(audio_segments)
    return transcriber.transcribe(source_lang)