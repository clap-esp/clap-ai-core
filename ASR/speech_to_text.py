import numpy as np

from typing import Tuple, List, Dict
from API.utils.logger import build_logger
from transformers import WhisperProcessor, TFWhisperForConditionalGeneration

logger = build_logger("SpeechToText", level=20)


def format_to_srt_time(seconds: float) -> str:
    """
    Formats time in seconds to SRT format HH:MM:SS,SSS.

    Parameters:
    - seconds: Time in seconds as a float.

    Returns:
    - str: Time formatted as HH:MM:SS,SSS.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


class STTTranscriber:
    """
    A class to handle Speech-to-Text transcription using a pre-trained model.

    Attributes:
    - model: The TFWhisperForConditionalGeneration model for transcription.
    - processor: The WhisperProcessor to preprocess inputs and decode outputs.
    - input_features: Cached input features from processed audio segments.
    """

    def __init__(self, model: TFWhisperForConditionalGeneration, processor: WhisperProcessor):
        """
        Initializes the STTTranscriber with a model, processor, and segment duration.

        Parameters:
        - model: A TFWhisperForConditionalGeneration model for transcription.
        - processor: WhisperProcessor to preprocess audio and decode model outputs.
        """
        self.model: TFWhisperForConditionalGeneration = model
        self.processor: WhisperProcessor = processor
        self.input_features = None
        self.segments = None

    def process_audio(self, segments: List[Tuple[float, np.ndarray]]):
        """
        Processes audio segments into input features for later transcription or translation.

        Parameters:
        - segments: List of tuples (start_time, audio_segment_data).
        """
        logger.info("Processing audio into input features...")
        self.segments = segments
        self.input_features = [
            self.processor(
                segment,
                sampling_rate=16_000,
                return_tensors="tf"
            ).input_features for _, segment in segments
        ]
        logger.info("Audio processing complete.")

    def transcribe(self, initial_lang: str) -> List[Dict[str, str]]:
        """
        Transcribes audio from pre-processed input features.

        Returns:
        - List of dictionaries containing transcription results.
        """
        logger.info("Starting transcription process...")
        if self.input_features is None:
            logger.error("No input features found. Run process_audio() first.")
            return []

        transcriptions = []
        for (start_time, _), features in zip(self.segments, self.input_features):
            predicted_ids = self.model.generate(features, language=initial_lang, return_timestamps=True,
                                                time_precision=0.02)
            result = self.processor.batch_decode(predicted_ids, output_offsets=True, skip_special_tokens=True)[0]

            for phrase in result['offsets']:
                phrase_start = start_time + phrase['timestamp'][0]
                phrase_end = start_time + phrase['timestamp'][1]
                transcriptions.append({
                    "start_time": format_to_srt_time(phrase_start),
                    "end_time": format_to_srt_time(phrase_end),
                    "duration": format_to_srt_time(phrase_end - phrase_start),
                    "transcription": phrase['text'],
                })

        logger.info("Transcription completed.")
        return transcriptions

    def translate(self, target_langs: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """
        Translates transcribed text into multiple target languages.

        Parameters:
        - target_langs: List of language codes for translation.

        Returns:
        - Dictionary mapping each language to a list of translated transcriptions.
        """
        logger.info("Starting translation process...")
        if self.input_features is None:
            logger.error("No input features found. Run process_audio() first.")
            return {}

        translations = {lang: [] for lang in target_langs}
        for (start_time, _), features in zip(self.segments, self.input_features):
            for lang in target_langs:
                predicted_ids = self.model.generate(features, language=lang)
                translated_text = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
                translations[lang].append({
                    "start_time": format_to_srt_time(start_time),
                    "translated_text": translated_text,
                    "translation_language": lang
                })

        logger.info("Translation completed.")
        return translations
