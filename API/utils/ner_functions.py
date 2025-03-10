import os
import logging
# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from transformers import BertTokenizerFast, TFBertForTokenClassification
import numpy as np
from sklearn.preprocessing import LabelEncoder

logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)


debug_mode = None
def log(message):
    if debug_mode:
        print(message)


MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'bert-base-multilingual-cased')
MODEL_ABSPATH = os.path.abspath(MODEL_PATH)

tokenizer = BertTokenizerFast.from_pretrained(MODEL_ABSPATH)
special_tokens_dict = {'additional_special_tokens': ['[bruit]', '<Silence>']} # the model can receive chosen tokens
num_added_toks = tokenizer.add_special_tokens(special_tokens_dict)

model = TFBertForTokenClassification.from_pretrained(MODEL_ABSPATH)
model.resize_token_embeddings(len(tokenizer)) # to include the special token


unique_labels = ['O', 'B-STU', 'I-STU', 'B-FIL', 'I-FIL', 'B-REP', 'I-REP', 'B-INT', 'I-INT', 'B-NOI', 'I-NOI', 'B-SIL', 'I-SIL']
label_encoder = LabelEncoder()
label_encoder.fit(unique_labels)


def process_ner(data):
    """ Processes a list of text segments for NER using fintuning BERT model
        Parameters: data (list of dict), where each dict must contain at least the keys 'text', 'time_start', and 'time_end'
        Returns: list of dict     
            {
                "time_start": 156.0,
                "time_end": 160.0,
                "text": "investir son temps",
                "words": [ "investir","son","temps" ],
                "labels": [ "O","O","O" ]
            },
        Note: If `debug_mode` is enabled for ex in test_app, additional information is printed for analyze intermediate results
    
    """
    print("\nProcessing NER in progress...")

    results = []

    for idx, segment in enumerate(data):
        text = segment['text']

        tokenized_input = tokenizer(
            text,
            add_special_tokens=True, # [CLS], [SEP]
            return_offsets_mapping=True, # to get the offset of each token
            return_tensors="tf",
            truncation=False,
            padding=False
        )

        input_ids = tokenized_input['input_ids']
        word_ids = tokenized_input.word_ids(batch_index=0)
        offset_mappings = tokenized_input['offset_mapping'][0]

        predictions = model(input_ids).logits

        label_indices = tf.math.argmax(predictions, axis=-1).numpy()[0] # get the index of the highest logit for each token
        
        # convert label indices to labels
        predicted_labels = label_encoder.inverse_transform(label_indices)
        predicted_labels = [str(label) for label in predicted_labels]

        tokens = tokenizer.convert_ids_to_tokens(input_ids[0])

        # group tokens by words and store their labels + offsets
        word_label_dict = {}
        word_offset_dict = {}

        for idx_token, (token, label, word_idx, offset) in enumerate(zip(tokens, predicted_labels, word_ids, offset_mappings)): # each token after tokenization
            if word_idx is None: # skip special tokens
                continue
            if word_idx not in word_label_dict:
                word_label_dict[word_idx] = []
                word_offset_dict[word_idx] = offset
            word_label_dict[word_idx].append(label)     
            word_offset_dict[word_idx] = (word_offset_dict[word_idx][0], offset[1]) # update -> the ending offset = the last token of this word
        # log(f"word_label_dict: {word_label_dict}")  # word_label_dict: {0: ['O'], 1: ['O'], 2: ['O'], 3: ['O'], 4: ['O'], 5: ['O', 'O', 'O'], 6: ['O', 'O']}

        # aggregate words and labels of each word
        words = []
        word_labels = []
        for word_idx in sorted(word_label_dict.keys()):
            labels = word_label_dict[word_idx]
            word_label = labels[0]  # assigns the first label of a word to the entire word
            word_labels.append(word_label)
            # extract the word from text using offsets
            start, end = word_offset_dict[word_idx]
            word = text[start:end]
            words.append(word)

        results.append({
            "time_start": segment["time_start"],
            "time_end": segment["time_end"],
            "text": text,
            "words": words,
            "labels": word_labels
        })

        if idx < 4:
            log(f"\n---> Line {idx+1}")
            log(f"- Original text: {text}")
            log(f"- Tokens after encoding: {tokens}")
            log(f"- Labels after encoding: {predicted_labels}")

    print("\nNER processing completed\n")
    return results