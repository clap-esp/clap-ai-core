import re
import json

class CompactJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, keys_to_compact=None, **kwargs):
        super().__init__(*args, **kwargs)
        if keys_to_compact is None:
            self.keys_to_compact = ['words', 'labels']
        else:
            self.keys_to_compact = keys_to_compact

    def encode(self, obj):
        json_str = super().encode(obj)
        
        def compact_array(match):
            """Method to compact specified arrays"""
            key = match.group(1)
            array_content = match.group(2)
            
            # removing unnecessary spaces
            array_content = re.sub(r'\s+', ' ', array_content)
            array_content = re.sub(r',\s+', ',', array_content)
            array_content = re.sub(r'\s+,', ',', array_content)
            return f'"{key}": [{array_content}]'
        
        # regex based on keys to compact
        keys_pattern = '|'.join(re.escape(key) for key in self.keys_to_compact)
        pattern = rf'"({keys_pattern})"\s*:\s*\[(.*?)\]'
        json_str = re.sub(pattern, compact_array, json_str, flags=re.DOTALL)
        
        return json_str
