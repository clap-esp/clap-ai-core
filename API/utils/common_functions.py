import json
from utils.compact_json_encoder import CompactJSONEncoder

def beautify_json(input_path, output_path):
    """Method to make json output more beautiful with compacting arrays"""
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    json_str = json.dumps(data, indent=4, ensure_ascii=False, cls=CompactJSONEncoder, keys_to_compact=['words', 'labels'])
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(json_str)