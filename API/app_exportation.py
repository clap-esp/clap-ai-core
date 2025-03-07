import os
import sys
import json
import time
import subprocess

# EXPORT DERUSHED VIDEO process - app
# This program is used to generate a "derushed" video (i.e., cuts validated by the user)

# How to run the script in your console (example):
#   python API/app_exportation.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4" "mp4" "16:9" "libx264" "path-de-destination"
#   python API/app_exportation.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4" "mov" "4:3" "prores"
#   python API/app_exportation.py "./video/Julie_Ng--Rain_rain_and_more_rain.mp4" "avi" "16:9" "mpeg4"

USER_CUTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp', 'user_cuts.json'))

debug_mode = False  # Debug mode setting

start_time = time.time()

# ↓ CHECK ARGS
if len(sys.argv) < 5:
    raise ValueError(
        "\nMissing arguments. \n"
        "Usage: python API/app_export_derush.py <video_path> <output_format> <aspect_ratio> <codec>\n"
        "Example: python API/app_export_derush.py \"./video/sample.mp4\" \"mp4\" \"16:9\" \"libx264\""
    )

video_path = sys.argv[1]
output_format = sys.argv[2]
video_aspect_ratio = sys.argv[3]
video_codec = sys.argv[4]  # codec vidéo

# ↓ CHECK VIDEO_PATH
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Error: Please check '{video_path}' path.")

# ↓ READ CUTS
if not os.path.exists(USER_CUTS_PATH):
    raise FileNotFoundError(f"Error: Please check '{USER_CUTS_PATH}' path.")

with open(USER_CUTS_PATH, 'r', encoding='utf-8') as json_file:
    selected_cuts = json.load(json_file)

if debug_mode:
    print(f"\n[DEBUG] Selected cuts => {selected_cuts}")

# ↓ CREATE EXPORT FOLDERS IF NEEDED
exports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports'))
os.makedirs(exports_dir, exist_ok=True)
tmp_dir = os.path.abspath(os.path.join(exports_dir, 'tmp_segments'))
os.makedirs(tmp_dir, exist_ok=True)

# ↓ PREPARE OUTPUT FILE NAME
timestamp_str = str(int(time.time()))
output_file_name = f"derushed_{timestamp_str}.{output_format}"
output_file_path = os.path.join(exports_dir, output_file_name)

# ↓ EXTRACT EACH CUT AND SAVE AS A TEMP SEGMENT
segment_list_file = os.path.join(tmp_dir, f"concat_list_{timestamp_str}.txt")

with open(segment_list_file, 'w', encoding='utf-8') as f_concat:
    for i, cut in enumerate(selected_cuts):
        start_time_sec = cut['start_time']
        duration = cut['duration']
        segment_path = os.path.join(tmp_dir, f"segment_{i}.{output_format}")

        # Build ffmpeg command for extracting a segment
        cmd_extract = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-ss", str(start_time_sec),
            "-i", video_path,
            "-t", str(duration),
            "-aspect", video_aspect_ratio,
            "-c:v", video_codec,
            "-c:a", "aac",
            "-strict", "experimental",
            segment_path
        ]

        if debug_mode:
            print(f"\n[DEBUG] Extract segment cmd => {' '.join(cmd_extract)}")

        subprocess.run(cmd_extract, check=True)

        # Write segment reference in the concat list file
        f_concat.write(f"file '{segment_path}'\n")

# ↓ CONCAT ALL SEGMENTS
cmd_concat = [
    "ffmpeg",
    "-hide_banner",
    "-loglevel", "error",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", segment_list_file,
    "-c", "copy",
    output_file_path
]

if debug_mode:
    print(f"\n[DEBUG] Concat segments cmd => {' '.join(cmd_concat)}")

subprocess.run(cmd_concat, check=True)

print(f"\nDerushed video exported => {output_file_path}")

# ↓ CLEAN-UP (AFTER...)
# import shutil
# shutil.rmtree(tmp_dir, ignore_errors=True)

print(f"\nEXPORT DERUSHED VIDEO SCRIPT took {int((time.time() - start_time) // 60)} minutes and {int((time.time() - start_time) % 60)} seconds")
