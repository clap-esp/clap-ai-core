import math
import librosa
import numpy as np

from typing import Tuple, List, Dict
from transformers import WhisperProcessor, WhisperForConditionalGeneration


def resample_audio(audio: Tuple[int, np.ndarray]) -> Tuple[int, np.ndarray]:
    """
    Resamples the audio to 16,000 Hz, ensures mono format, and normalizes it.

    Parameters:
    - audio: Tuple containing the sample rate (int) and audio data (np.ndarray).

    Returns:
    - Tuple: Resampled audio with a new sample rate and normalized audio array.
    """
    sr, y = audio

    # Convert to mono if stereo
    if y.ndim > 1:
        y = y.mean(axis=1)

    # Ensure the audio is in floating-point format
    y = y.astype(np.float32)

    # Resample to 16, 000Hz if necessary
    if sr != 16000:
        y = librosa.resample(y, orig_sr=sr, target_sr=16000)
        sr = 16000

    # Normalize the audio
    y /= np.max(np.abs(y))
    return sr, y


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
    - model: The WhisperForConditionalGeneration model for transcription.
    - processor: The WhisperProcessor to preprocess inputs and decode outputs.
    - segment_duration: Duration (in seconds) of each audio segment.
    """

    def __init__(self, model, processor, segment_duration=30):
        """
        Initializes the STTTranscriber with a model, processor, and segment duration.

        Parameters:
        - model: A WhisperForConditionalGeneration model for transcription.
        - processor: WhisperProcessor to preprocess audio and decode model outputs.
        - segment_duration: The duration (in seconds) for each audio segment.
        """
        self.model: WhisperForConditionalGeneration = model
        self.processor: WhisperProcessor = processor
        self.segment_duration = segment_duration

    def split_audio(self, audio: Tuple[int, np.ndarray]) -> List[Tuple[float, np.ndarray]]:
        """
        Splits the audio into fixed-duration segments due to Whisper 30 seconds chunk limitation.

        Parameters:
        - audio: Tuple containing the sample rate and audio data as a NumPy array.

        Returns:
        - List of tuples with start time (in seconds) and audio segment data.
        """
        sr, y = audio
        segment_length = self.segment_duration * sr
        num_segments = math.ceil(len(y) / segment_length)

        segments = []
        for i in range(num_segments):
            start_time = i * self.segment_duration
            end_sample = min((i + 1) * segment_length, len(y))
            segments.append((start_time, y[i * segment_length:end_sample]))

        return segments

    def transcribe(self, audio: Tuple[int, np.ndarray], target_langs: List[str] = ["fr"]): # -> Dict[str, List[Dict[str, str]]]:
        """
        Transcribes and translates audio into multiple languages.

        Parameters:
        - audio: Tuple containing the sample rate and audio data as a NumPy array.
        - target_langs: List of target language codes for translation.

        Returns:
        - Tuple containing:
          - Dictionary of transcriptions with language codes as keys and texts as values.
          - Dictionary of transcription segments with start and end times.
        """
        print("Starting to transcribe...")

        if audio is None:
            print("No audio input received. Please provide a valid audio file.")
            return {}, {}

        sr, y = resample_audio(audio)

        # Split audio into segments
        audio_segments = self.split_audio((sr, y))

        results = {lang: [] for lang in target_langs}
        transcription_data = {lang: [] for lang in target_langs}

        try:
            for start_time, segment in audio_segments:
                # Prepare the input features
                input_features = self.processor(
                    segment,
                    sampling_rate=sr,
                    return_tensors="pt"
                ).input_features

                for lang in target_langs:
                    # Generate the transcription
                    predicted_ids = self.model.generate(
                        input_features,
                        language=lang,
                        return_timestamps=True,
                        time_precision=0.02,
                        return_token_timestamps = True,
                    )


                    result = self.processor.batch_decode(
                        predicted_ids["sequences"],
                        output_offsets=True,
                        skip_special_tokens=True,
                        decode_with_timestamps=False
                    )[0]


                    transcription_data[lang].append(result["text"])
                    print(f"Result for {lang}: {result}")

                    for phrase in result['offsets']:
                        phrase_start = start_time + phrase['timestamp'][0]
                        phrase_end = start_time + phrase['timestamp'][1]
                        results[lang].append({
                            "start_time": format_to_srt_time(phrase_start),
                            "end_time": format_to_srt_time(phrase_end),
                            "transcription": phrase['text']
                        })
            print(results)
            return transcription_data, results

        except Exception as e:
            print(f"An error occurred during transcription: {str(e)}")
            return f"An error occurred during transcription: {str(e)}"
