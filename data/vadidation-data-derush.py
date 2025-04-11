import os
import ast
import pandas as pd
import csv
import ast


# VALIDATION test
# This program is used for test and automates the checking of human errors in datasets.

train_path = os.path.join(os.path.dirname(__file__), "./train-data-derush.csv")
test_path = os.path.join(os.path.dirname(__file__), "./test-data-derush.csv")
absolute_train_path = os.path.abspath(train_path)
absolute_test_path = os.path.abspath(test_path)

# Constants for validation
AUTHORIZED_LABELS = ["O", "B-STU", "I-STU", "B-FIL", "I-FIL", "B-REP", "I-REP", "B-INT", "I-INT", "B-NOI", "I-NOI", "B-SIL", "I-SIL"]
PUNCTUATION_ITEMS = [",", ".", "!", "?", ";", ":", "'", '"', "(", ")", "{", "}"]


# def read_dataset(csv_file_path):
#     """Read and parse the dataset from a CSV file into a list of dictionaries."""
#     data = []
#     df = pd.read_csv(csv_file_path, skipinitialspace=True).fillna("")
#     for index, row in df.iterrows():
#         data.append({
#             "phrase": row["phrase"],
#             "items": ast.literal_eval(row["items"]),
#             "labels": ast.literal_eval(row["labels"])
#         })
# return data

def read_dataset(csv_file_path):
    import os
    print("Trying to open:", csv_file_path)
    print("File exists?", os.path.exists(csv_file_path))

    data = []
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        lines = csvfile.readlines()
        print("Nombre de lignes lues :", len(lines))
        # for i, line in enumerate(lines, start=1):
        #     print(f"Ligne {i} => {repr(line)}")

        csvfile.seek(0)  # Reset file pointer to the beginning of the file after reading lines
        reader = csv.reader(csvfile)
        header = next(reader)
        print("Header =", header)

        expected_columns = len(header)
        line_number = 2  # The header is already read, so we start at line 2
        
        for row in reader:
            if len(row) != expected_columns:
                print(f"error of column count at line {line_number}: expected {expected_columns}, found {len(row)}")
            else:
                try:
                    data.append({
                        "phrase": row[0],
                        "items": ast.literal_eval(row[1]),
                        "labels": ast.literal_eval(row[2])
                    })
                except Exception as e:
                    print(f"Error parsing data at line {line_number}:\n  → row={row}\n  → {e}")
            line_number += 1
    return data


def check_items_labels_length(data):
    """Verify that the number of items matches the number of labels for each entry"""
    errors = []
    for idx, entry in enumerate(data):
        if len(entry["items"]) != len(entry["labels"]):
            errors.append(f"Error in entry {idx}: Number of items does not match number of labels")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed items-labels length check")


def check_authorized_labels(data):
    """Ensure each label used is within the authorized set of labels"""
    errors = []
    for idx, entry in enumerate(data):
        for label in entry["labels"]:
            if label not in AUTHORIZED_LABELS:
                errors.append(f"Error in entry {idx}: Label '{label}' is not an authorized label")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed authorized labels check")



def check_label_sequence(data):
    """Ensure 'B-' labels are correctly followed by 'I-' labels of the same type or by 'O'"""
    errors = []
    for idx, entry in enumerate(data):
        labels = entry["labels"]
        for i in range(len(labels) - 1):
            if labels[i].startswith("B-") and labels[i+1].startswith("I-") and labels[i][2:] != labels[i+1][2:]:
                errors.append(f"Error in entry {idx}, token {i+1}: Incorrect sequence of labels '{labels[i]}' followed by '{labels[i+1]}'")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed label sequence check")


def check_triple_dot_sequence(data):
    """Check that each sequence of ('.', '.', '.') is annotated B-SIL, I-SIL, I-SIL in the correct order"""
    errors = []
    for idx, entry in enumerate(data):
        items = entry["items"]
        labels = entry["labels"]
        i = 0
        while i < len(items) - 2:
            if items[i] == "." and items[i+1] == "." and items[i+2] == ".":
                if not (labels[i] == "B-SIL" and labels[i+1] == "I-SIL" and labels[i+2] == "I-SIL"):
                    errors.append(
                        f"Error in entry {idx}, tokens {i}-{i+2}: "
                        f"Triple dot sequence must be labeled B-SIL, I-SIL, I-SIL. Found {labels[i]}, {labels[i+1]}, {labels[i+2]}"
                    )
                i += 3
            else:
                i += 1

    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed triple dot sequence check")


def check_punctuation_labels(data):
    """Check that the punctuation marks are correctly annotated "O" — EXCEPT the special case where there is a ..."""
    errors = []
    for idx, entry in enumerate(data):
        items = entry["items"]
        labels = entry["labels"]
        i = 0
        while i < len(items):
            if items[i] in PUNCTUATION_ITEMS:
                if (
                    items[i] == "."
                    and i <= len(items) - 3
                    and items[i+1] == "."
                    and items[i+2] == "."
                ):
                    i += 3
                    continue
                else:
                    if labels[i] != "O":
                        errors.append(
                            f"Error in entry {idx}, token {i}: "
                            f"Punctuation item '{items[i]}' should be annotated as 'O' (found '{labels[i]}')"
                        )
            i += 1

    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed punctuation labels check")


def check_bruit_annotation(data):
    """
    Check that each occurrence of '[Bruit]' is correctly annotated by 'B-NOI' or 'I-NOI'
    """
    errors = []
    for idx, entry in enumerate(data):
        for item, label in zip(entry["items"], entry["labels"]):
            if item == "[Bruit]" and label not in ["B-NOI", "I-NOI"]:
                errors.append(f"Error in entry {idx}: '[Bruit]' should be annotated as 'B-NOI' or 'I-NOI'")
    if errors:
        for error in errors:
            print(error)
    else:
        print("All entries passed [Bruit] annotation check")


if __name__ == "__main__":
    print("\n-- Checking TRAIN dataset --")
    train_data = read_dataset(absolute_train_path)
    check_items_labels_length(train_data)
    check_authorized_labels(train_data)
    check_punctuation_labels(train_data)
    check_label_sequence(train_data)
    check_triple_dot_sequence(train_data)
    check_bruit_annotation(train_data)

    print("\n-- Checking TEST dataset --")
    test_data = read_dataset(absolute_test_path)
    check_items_labels_length(test_data)
    check_authorized_labels(test_data)
    check_punctuation_labels(test_data)
    check_label_sequence(test_data)
    check_triple_dot_sequence(test_data)
    check_bruit_annotation(test_data)
