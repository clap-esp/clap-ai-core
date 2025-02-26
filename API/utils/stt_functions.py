import os
import math
import speech_recognition as sr
from pydub import AudioSegment

from transformers import WhisperForConditionalGeneration, WhisperProcessor

from ASR.speech_to_text import STTTranscriber
from API.utils.audio_extractor import extract_audio_features

debug_mode = None
def log(message):
    if debug_mode:
        print(message)


def process_stt(model: WhisperForConditionalGeneration, processor: WhisperProcessor, video_path: str, source_lang: str = "fr"): # for whisper
    transcriber = STTTranscriber(model=model, processor=processor)

    audio_segments = extract_audio_features(video_path, use_effect_split=True)
    transcriber.process_audio(audio_segments)
    return transcriber.transcribe(source_lang)


def process_stt_deprecated(audio_file_path, chunk_length_ms=4000):
    """Process the audio file and return a list of transcribed sentences with timestamps"""
    print(f"Processing audio file: {audio_file_path}")
    print(f"Processing in progress...")

    chunks_dir = os.path.join(os.getcwd(), "chunks")
    create_chunks_directory(chunks_dir)

    audio = AudioSegment.from_wav(audio_file_path)

    # calculate number of chunks
    audio_length_ms = len(audio)
    num_chunks = math.ceil(audio_length_ms / chunk_length_ms)
    log(f"\nNumber of segments: {num_chunks}")
    log(f"Print each segment in terminal:")

    recognizer = sr.Recognizer()
    results = []

    for i in range(num_chunks):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, audio_length_ms)
        chunk = audio[start_ms:end_ms]
        chunk_filename = os.path.join(chunks_dir, f"chunk_{i}.wav")

        chunk.export(chunk_filename, format="wav")  # export the chunk

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
            text = recognize(audio_data, recognizer)

            if text:  # only add to results if text was recognized
                result = {
                    "time_start": start_ms / 1000.0,  # Convert ms to seconds
                    "time_end": end_ms / 1000.0,
                    "text": text
                }
                results.append(result)

            log(f"{i}. {text}")

        os.remove(chunk_filename) # remove the chunk file as progresses

    return results


def recognize(audio_data, recognizer, language='fr-FR'):
    """Method to recognize speech with audio chunk."""
    try:
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        return "[Bruit]" # by default... this is temporary !!!
    except sr.RequestError as e:
        return f"Error requesting Google service: {e}"

def create_chunks_directory(dir_path):
    """Create the audio segment directory."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)