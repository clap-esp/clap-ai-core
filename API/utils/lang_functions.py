import os
from deep_translator import GoogleTranslator

def translate_srt_file(input_path, output_path, src_lang, dest_lang):
    print(f"Translating {input_path} -> {src_lang}")
    print(f"Output file: {output_path} -> {dest_lang}")
    # open both the input and output files
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            striped = line.strip()
            # check if the line is a number, timecode, or empty
            if striped.isdigit() or '-->' in striped or striped == '':
                outfile.write(line)  # write this line
            else:
                # translate the text line and write the result
                if striped:  # is not empty
                    translated_text = GoogleTranslator(source=src_lang, target=dest_lang).translate(striped)
                    outfile.write(translated_text + '\n')
                else:
                    outfile.write('\n')  # write an empty line if the original line was empty



# def multilang_srt(data_multilang, output_folder="srt_files"):
#     os.makedirs(output_folder, exist_ok=True)
    
#     if os.path.exists(output_folder):
#         print(f"Dossier '{output_folder}' existe déjà ou a été créé.")

#     srt_files = {}
    
#     for lang_data in data_multilang:
#         lang = lang_data["lang"]
#         filename = f"{output_folder}/subtitles_{lang}.srt"
        
#         if os.path.exists(filename):
#             print(f"Fichier '{filename}' existe déjà.")
#         else:
#             print(f"Création du fichier '{filename}'.")

#         srt_content = ""
#         for i, item in enumerate(lang_data["transcription"], start=1):
#             srt_content += f"{i}\n"
#             srt_content += f"{item['start_time']} --> {item['end_time']}\n"
#             srt_content += f"{item['subtitles']}\n\n"
        
#         with open(filename, mode="w", encoding="utf-8") as file:
#             file.write(srt_content)
        
#         srt_files[lang] = filename

#     return srt_files

# data_multilang = [
#     {
#         "lang": "en",
#         "transcription": [
#             {
#                 "start_time": "00:05:00,400",
#                 "end_time": "00:05:15,300",
#                 "subtitles": "This is an example of a subtitle.",
#             },
#             {
#                 "start_time": "00:05:16,400",
#                 "end_time": "00:05:25,300",
#                 "subtitles": "This is an example of a subtitle - 2nd subtitle.",
#             },
#         ]
#     },
#     {
#         "lang": "fr",
#         "transcription": [
#             {
#                 "start_time": "00:05:00,400",
#                 "end_time": "00:05:15,300",
#                 "subtitles": "Ceci est un exemple de sous-titre.",
#             },
#             {
#                 "start_time": "00:05:16,400",
#                 "end_time": "00:05:25,300",
#                 "subtitles": "Ceci est un exemple de sous-titre - 2e sous-titre.",
#             },
#         ]
#     },
# ]

# srt_files = multilang_srt(data_multilang)
# #for lang, file_path in srt_files.items():
#     #print(f"SRT file for {lang} generated at: {file_path}")