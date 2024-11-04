# This test script is intended to automate the checking of human errors in datasets.
import os
import csv
import ast
import pandas as pd

# access csv
train_path = os.path.join(os.path.dirname(__file__), 'train-data-derush.csv')
test_path = os.path.join(os.path.dirname(__file__), 'test-data-derush.csv')
absolute_train_path = os.path.abspath(train_path)
absolute_test_path = os.path.abspath(test_path)

AUTHORIZED_LABELS = ['O', 'B-STU', 'I-STU', 'B-FIL', 'I-FIL', 'B-REP', 'I-REP', 'B-INT', 'I-INT', 'B-NOI', 'I-NOI', 'B-SIL', 'I-SIL']
PUNCTUATION_ITEMS = [',', '.', '!', '?', ';', ':', '...', "'", '"', '(', ')', '{', '}']

def read_dataset(csv_file_path):
    data = []
    df = pd.read_csv(csv_file_path).fillna('')
   
    for  index, row in df.iterrows():
        phrase = row['phrase']
        items = ast.literal_eval(row['items'])
        labels = ast.literal_eval(row['labels'])
        data.append({'phrase': phrase, 'items': items, 'labels': labels})
    return data

# Function to check that the number of items matches the number of labels
def check_items_labels_length(data):
    errors = []
    for idx, entry in enumerate(data):
        items = entry['items']
        labels = entry['labels']
        if len(items) != len(labels):
            errors.append(f"Error in entry {idx}: Number of items {len(items)} does not match number of labels {len(labels)}")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed items-labels length check")

# Function to check that each label is in the list of authorized labels
def check_authorized_labels(data):
    errors = []
    for idx, entry in enumerate(data):
        labels = entry['labels']
        for label in labels:
            if label not in AUTHORIZED_LABELS:
                errors.append(f"Error in entry {idx}: Label '{label}' is not an authorized label")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed authorized labels check")

# Function to check that punctuation items are correctly annotated by 'O'
def check_punctuation_labels(data):
    errors = []
    for idx, entry in enumerate(data):
        items = entry['items']
        labels = entry['labels']
        for item, label in zip(items, labels):
            if item in PUNCTUATION_ITEMS and label != 'O':
                errors.append(f"Error in entry {idx}: Punctuation item '{item}' should be annotated as 'O' but got '{label}'")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed punctuation labels check")


if __name__ == "__main__":
    print("Checking train dataset")
    train_data = read_dataset(absolute_train_path)
    check_items_labels_length(train_data)
    check_authorized_labels(train_data)
    check_punctuation_labels(train_data)

    print("\nChecking test dataset")
    test_data = read_dataset(absolute_test_path)
    check_items_labels_length(test_data)
    check_authorized_labels(test_data)
    check_punctuation_labels(test_data)

# to do
# check la gestion des apostrophes
# check les [] et à voir pour les inclure dans les B-NOI et I-NOI
