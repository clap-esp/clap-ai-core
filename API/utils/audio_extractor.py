import os
import librosa
import numpy as np

from typing import Tuple, List, Union
from tempfile import NamedTemporaryFile

from API.utils.logger import build_logger
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip


logger = build_logger("Audio_Extractor", level=20)
output_audio_path = os.path.join(os.path.dirname(__file__), '..', 'audio_before_derush', 'audio_extrait.wav')

def extract_audio_from_video(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path, codec='pcm_s16le')  # WAV format
    video.close()
    audio.close()


def extract_audio(file_path: Union[str, Tuple[int, np.ndarray]]) -> Tuple[np.ndarray, int | float]:
    """
        Extracts audio from a given video file and returns the waveform and sample rate.

        This function loads a video file, extracts its audio, and converts it into a format suitable
        for further processing. The extracted audio is saved temporarily before being loaded into
        a NumPy array using Librosa.

        :param file_path: Path to the video file.
        :return: A tuple containing:
                 - A NumPy array representing the audio waveform.
                 - The sample rate of the extracted audio.
    """
    logger.info(f"Extracting audio from: {file_path}")

    video_clip = VideoFileClip(file_path)
    audio_clip: AudioFileClip = video_clip.audio

    with NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
        audio_clip.write_audiofile(
            temp_audio_file.name,
            codec='pcm_s16le',
            fps=44100
        )
        video_clip.close()
        audio_clip.close()
        audio_data = librosa.load(temp_audio_file.name, sr=16000)
    return audio_data


def split_audio_samples(
        samples: np.ndarray,
        sample_rate: int,
        segment_duration: int = 30
) -> List[Tuple[float, np.ndarray]]:
    """
        Splits audio samples into fixed 30s segments.

        :param samples: NumPy array containing audio waveform.
        :param sample_rate: Sampling rate of the audio.
        :param segment_duration: Target duration for each segment in seconds (default: 30s).
        :return: List of tuples containing (start_time, audio_segment_data).
    """
    logger.info("Starting fixed 30s audio segmentation")
    segments = []
    start_sample = 0

    while start_sample < len(samples):
        end_sample = start_sample + (segment_duration * sample_rate)
        if end_sample >= len(samples):
            end_sample = len(samples)

        segment = samples[start_sample:end_sample]
        start_time = start_sample / sample_rate
        segments.append((start_time, segment))

        logger.info(f"Segment start: {start_time:.2f}s, end: {end_sample / sample_rate:.2f}s")

        start_sample = end_sample

    logger.info(f"Extracted {len(segments)} segments.")
    return segments


def split_audio_samples_with_effect_split(
        samples: np.ndarray,
        sample_rate: int,
        silence_threshold: int = 30,
        # silence_threshold: int = 40,
        segment_duration_limit: int = 30,
) -> List[Tuple[float, np.ndarray]]:
    """
        Splits audio samples using silence detection to find non-silent intervals.
        Ensures segments do not exceed a given duration.

        :param samples: NumPy array containing audio waveform.
        :param sample_rate: Sampling rate of the audio.
        :param silence_threshold: Threshold in dB to detect silence.
        :param segment_duration_limit: Maximum duration of an audio segment in seconds.
        :return: List of tuples containing (start_time, audio_segment_data).
        """
    logger.info("Starting audio segmentation using silence detection")

    max_val = np.max(np.abs(samples))
    if max_val > 0:
        samples /= max_val
    else:
        logger.warning("Audio samples contain only silence or zero values.")

    non_silent_parts = librosa.effects.split(samples, top_db=silence_threshold)
    logger.info(f"Detected {len(non_silent_parts)} non-silent segments.")

    # Generate audio segments
    segments = []
    for start_sample, end_sample in non_silent_parts:
        start_time = start_sample / sample_rate
        end_time = end_sample / sample_rate

        segment_duration = end_time - start_time
        segment = samples[start_sample:end_sample]

        if segment_duration > segment_duration_limit:
            num_sub_segments = int(np.ceil(segment_duration / segment_duration_limit))
            chunk_size = int(segment_duration_limit * sample_rate)

            for i in range(num_sub_segments):
                sub_start = i * chunk_size
                sub_end = min((i + 1) * chunk_size, len(segment))
                sub_segment = segment[sub_start:sub_end]
                sub_start_time = start_time + (sub_start / sample_rate)
                segments.append((sub_start_time, sub_segment))
        else:
            segments.append((start_time, segment))

    logger.info(f"Extracted a total of {len(segments)} segments.")
    return segments


def extract_audio_features(
        file_path: Union[str, Tuple[int, np.ndarray]],
        segment_duration: int = 30,
        use_effect_split: bool = True
) -> List[Tuple[float, np.ndarray]]:
    """
        Extracts and processes audio from a video file.
        Splits into fixed-duration segments (default 30s).

        :param file_path: Path to the video/audio file.
        :param segment_duration: Fixed duration for segmentation (default: 30s).
        :param use_effect_split: If True, uses silence-based segmentation instead of fixed-duration segmentation.
        :return: List of tuples containing (start_time, audio_segment_data).
    """

    try:
        samples, sample_rate = extract_audio(file_path)

        logger.info(f"Starting to extract features from: {file_path}")

        if use_effect_split:
            segments = split_audio_samples_with_effect_split(samples, sample_rate)
        else:
            segments = split_audio_samples(samples, sample_rate, segment_duration)

        return segments

    except Exception as e:
        logger.error(f"Error extracting audio: {e}")
        return []
