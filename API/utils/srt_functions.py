import re


def seconds_to_srt_time(seconds):
    """Convert time in seconds (float) to SRT format hh:mm:ss,mmm"""
    heures = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secondes = int(seconds % 60)
    millisecondes = int((seconds - int(seconds)) * 1000)
    return f"{heures:02}:{minutes:02}:{secondes:02},{millisecondes:03}"

def json_to_srt_derush(json_data):
    """Converts a JSON structure to SRT subtitles format
        json_data
            {
                "start_time": float,
                "duration": float,
                "words": [string...]
            }
    """
    print("\nSubtitles conversion in progress...")
    srt_lines = []
    for i, segment in enumerate(json_data, start=1):
        start = segment["start_time"]
        duration = segment["duration"]
        end = start + duration
        words = segment["words"]
        
        start_str = seconds_to_srt_time(start)
        end_str = seconds_to_srt_time(end)
        
        subtitle_text = " ".join(words)
        subtitle_text = re.sub(r"\s+'\s+", "'", subtitle_text) # remove spaces before apostrophes
        
        srt_lines.append(str(i))  # subtitle number
        srt_lines.append(f"{start_str} --> {end_str}")
        srt_lines.append(subtitle_text)
        srt_lines.append("")  # blank line after each subtitle
    
    return "\n".join(srt_lines)


def json_to_srt_transcription(json_data):
    """Converts a JSON structure to SRT subtitles format
        json_data
        {
            "time_start": float,
            "time_end": float,
            "text": "bienvenue tout le monde dans ce talk"
        }
    """
    print("\nSubtitles conversion in progress...")
    srt_lines = []
    for i, segment in enumerate(json_data, start=1):
        start = segment["time_start"]
        end = segment["time_end"]
        text = segment["text"]

        start_str = seconds_to_srt_time(start)
        end_str = seconds_to_srt_time(end)

        # clean up the text by removing unwanted spaces around punctuation
        subtitle_text = re.sub(r"\s+'\s+", "'", text)  # remove spaces before apostrophes
        subtitle_text = re.sub(r" \.", ".", subtitle_text)  # before periods
        subtitle_text = re.sub(r" \,", ",", subtitle_text)  # before commas
        subtitle_text = re.sub(r" \!", "!", subtitle_text)  # before exclamations

        srt_lines.append(str(i))  # subtitle number
        srt_lines.append(f"{start_str} --> {end_str}")
        srt_lines.append(subtitle_text)
        srt_lines.append("")  # blank line after each subtitle

    return "\n".join(srt_lines)
