import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc


def load_data(train_file, test_file):
    data_train = pd.read_csv(train_file).fillna('')
    data_test = pd.read_csv(test_file).fillna('')
    return data_train, data_test

def prepare_labels(unique_labels):
    label_encoder = LabelEncoder()
    label_encoder.fit(unique_labels)
    print("Mapping labels and IDs:\n", {label: idx for idx, label in enumerate(label_encoder.classes_)})
    return label_encoder

def evaluate_model(model, test_tokens, test_labels):
    evaluation_results = model.evaluate(test_tokens, test_labels)
    print("\n// Results:", evaluation_results)
    test_predictions = model.predict(test_tokens).logits
    predicted_labels = np.argmax(test_predictions, axis=-1).flatten()
    true_labels = test_labels.flatten()
    return evaluation_results, predicted_labels, true_labels

def save_model(model, tokenizer, model_save_path):
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"\n// Model and tokenizer saved")

def encode_data(data, tokenizer, label_encoder, max_length=36):
    tokens = []
    labels = []

    for i, row in data.iterrows():
        items = eval(row['items'])
        word_labels = eval(row['labels'])

        if len(items) != len(word_labels):
            print(f"The length of the elements ({len(items)}) does not match the length of the labels ({len(word_labels)}) on line {i+1}")
            continue

        if i < 4:
            print(f"\n---> Ligne {i+1}")
            print("- Original items: ", items)

        tokenized_input = tokenizer(
            items,
            is_split_into_words=True,
            add_special_tokens=True,  # [CLS] at the beginning and [SEP] at the end
            return_offsets_mapping=True,
            return_tensors="tf",  # returns tokens to tensors
            max_length=max_length,
            truncation=True,  # if the sentence is longer than max_length
            padding="max_length"  # so that all sequences have the same number of tokens
        )

        input_ids = tokenized_input['input_ids'][0] # IDs of tokens
        word_ids = tokenized_input.word_ids(batch_index=0) # Mapping token to IDs

        if i < 4:
            print("- Tokens after encodage: ", tokenizer.convert_ids_to_tokens(input_ids))

        label_ids = [] # Initialised the list of labels for the tokens

        previous_word_idx = None
        for idx, word_idx in enumerate(word_ids):
            if word_idx is None:
                label_ids.append(label_encoder.transform(['O'])[0])  # Tokens de padding
            elif word_idx < len(word_labels):
                label = word_labels[word_idx]
                if word_idx != previous_word_idx:
                    # First token of a word
                    label_id = label_encoder.transform([label])[0]
                else:
                    # Subsequent tokens of a word
                    if label == 'O':
                        sub_label = 'O'
                    elif label.startswith('B-'):
                        sub_label = 'I-' + label[2:]
                    elif label.startswith('I-'):
                        sub_label = label  # Keep the same label
                    else:
                        sub_label = label
                    label_id = label_encoder.transform([sub_label])[0]
                label_ids.append(label_id)
                previous_word_idx = word_idx
            else:
                # If the word_idx is greater than the length of word_labels
                print(f"Avertissement : word_idx ({word_idx}) dépasse la longueur de word_labels ({len(word_labels)}) à la ligne {i+1}")
                label_ids.append(label_encoder.transform(['O'])[0])  # Assign 'O' label by default

        tokens.append(input_ids.numpy())
        labels.append(label_ids)

        if i < 4:
            label_list = label_encoder.inverse_transform(label_ids)
            print("- Labels after encodage: ", label_list)

    print("\n// Encoding completed //\n")
    return np.array(tokens), np.array(labels)


def get_metrics(y_true, y_pred, labels):
    # Flatten the lists
    y_true_flat = [label for sublist in y_true for label in sublist]
    y_pred_flat = [label for sublist in y_pred for label in sublist]

    cm = confusion_matrix(y_true_flat, y_pred_flat, labels=range(len(labels)))
    print("\nConfusion matrix:")
    print(cm)

    print("\nConfusion matrix with percent:")
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm_norm, annot=True, fmt=".2f", cmap="Blues", xticklabels=labels, yticklabels=labels, square=True)
    plt.title('Matrice de Confusion')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='normal')
    plt.yticks(fontsize=10, fontweight='normal')
    plt.show()

    print("\nClassification report:")
    print(classification_report(y_true_flat, y_pred_flat, target_names=labels))


def plot_training_history(history):
    """
    Displays the evolution of accuracy and loss over time from a History object
    """
    print("\nEvolution of accuracy and loss over the epoch:")
    if history is not None:
        plt.figure(figsize=(12, 5))

        # accuracy
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Training accuracy', marker='o')
        plt.plot(history.history['val_accuracy'], label='Validation accuracy', marker='o')
        plt.title('Model accuracy over epochs')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()

        # loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Training loss', marker='o')
        plt.plot(history.history['val_loss'], label='Validation loss', marker='o')
        plt.title('Model loss over epochs')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()

        plt.tight_layout()
        plt.show()

def get_ROC_curve(true_labels, logits, unique_labels):
    """
    Generate and display ROC curves for each class, as well as a micro-average
    for the true_labels (in [batch, sequence_length] format) and the raw logits
    of the model (in [batch, sequence_length, num_classes] format).
    """    
    y_true_flat = true_labels.reshape(-1)
    probabilities = tf.nn.softmax(logits, axis=-1).numpy()
    num_classes = len(unique_labels)
    probabilities = probabilities.reshape(-1, num_classes)
    y_true_bin = label_binarize(y_true_flat, classes=range(num_classes))
    
    fpr = {}
    tpr = {}
    roc_auc = {}
    
    for i in range(num_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], probabilities[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), probabilities.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    # Affichage
    print("\nROC AUC curve:")
    plt.figure(figsize=(8, 6))
    
    plt.plot(fpr["micro"], tpr["micro"], 
             label='micro-average (AUC = {0:0.2f})'.format(roc_auc["micro"]))
    
    for i, label_name in enumerate(unique_labels):
        plt.plot(fpr[i], tpr[i],
                 label='{} (AUC = {:0.2f})'.format(label_name, roc_auc[i]))
    
    plt.plot([0, 1], [0, 1], 'r--', lw=2)
    
    plt.title("Courbes ROC multiclasse (One-vs-Rest)")
    plt.xlabel("Taux de Faux Positifs (FPR)", fontsize=12)
    plt.ylabel("Taux de Vrais Positifs (TPR)", fontsize=12)
    plt.legend(loc="lower right", fontsize=9)
    plt.show()