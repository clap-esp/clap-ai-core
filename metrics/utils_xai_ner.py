
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf


def visualize_attention(text, model, tokenizer, model_name):
    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////")
    print(f"\n---   Phrase : \n---> '{text}'\n")
    print(f"\nIci on voit sur quels tokens d'entrées {model_name} porte son attention pour chaque token de sortie. Pour produire son embedding.")
    # generate the outputs with the attentions
    inputs = tokenizer.encode_plus(text, return_tensors='tf')
    outputs = model(**inputs, output_attentions=True)
    attentions = outputs.attentions  # (num_layers, batch, num_heads, seq_len, seq_len)
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0].numpy())

    total_layers = len(attentions)
    # select the last 5 layers
    last_5_attentions = attentions[-5:]
    num_layers = len(last_5_attentions)

    # 1 heatmap par couche
    fig, axes = plt.subplots(1, num_layers, figsize=(4 * num_layers, 4))
    if num_layers == 1:
        axes = [axes]

    for layer_idx, layer_attention in enumerate(last_5_attentions):
        layer_attention = tf.squeeze(layer_attention, axis=0)  # (num_heads, seq_len, seq_len)
        layer_attention_mean = tf.reduce_mean(layer_attention, axis=0).numpy()

        ax = axes[layer_idx]
        sns.heatmap(
            layer_attention_mean, 
            xticklabels=tokens, 
            yticklabels=tokens, 
            cmap='viridis', 
            ax=ax
        )
        # The layer index here is relative to the last 5 layers
        absolute_layer_index = (len(attentions) - 5 + layer_idx + 1)
        ax.set_title(f'Layer {absolute_layer_index}', fontsize=12)
        ax.set_xlabel('Input Tokens', fontsize=10)
        ax.set_ylabel('Output Tokens', fontsize=10)
        # Label rotation
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    fig.suptitle(f"Last 5 layers attention weights for {model_name}", fontsize=16)
    plt.tight_layout()
    plt.show()
    print("Nombre total de layers:", total_layers)



def print_predict_duration(total_start_time, total_end_time):
    total_predict_duration = total_end_time - total_start_time
    seconds = int(total_predict_duration)
    milliseconds = (total_predict_duration - seconds) * 1000
    print(f"\n⏱️ Total prediction time: {seconds} seconds and {milliseconds:.2f} milliseconds")
    return total_predict_duration