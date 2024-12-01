# Copyright (c) Microsoft Corporation. All rights reserved.
from transformers import AutoModelForCausalLM, AutoTokenizer

import transformers
import torch

model = "/home/edu/.llama/checkpoints/Llama3.2-1B"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model)
# Generate text
input_text = "What is the capital of France?"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs["input_ids"], max_length=50)
# Print the result
print(tokenizer.decode(outputs[0], skip_special_tokens=True))