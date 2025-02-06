import pandas as pd
from transformers import RobertaTokenizerFast
import torch
import sys

# Initialize the RoBERTa tokenizer
tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base')

# Move the model to the GPU (if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define a function to count the number of tokens in a prompt
def count_tokens(prompt):
    return len(tokenizer.encode(prompt))

if __name__ == "__main__":
    # Check if the prompt is provided as a command line argument
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        tokens_count = count_tokens(prompt)
        print(tokens_count)
    else:
        print("Please provide a prompt as a command line argument.")
