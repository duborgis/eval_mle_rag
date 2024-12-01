from transformers import AutoModelForCausalLM, AutoTokenizer

HF_TOKEN = "HAHAHA_NOPE"

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    device_map="auto",
    load_in_4bit=True,
    use_auth_token=HF_TOKEN,  # Add the token here
)

tokenizer = AutoTokenizer.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    padding_side="left",
    use_auth_token=HF_TOKEN,  # Add the token here
)

model_inputs = tokenizer(["Qual o nome do seu criador?"], return_tensors="pt").to("cuda")

outputs = model.generate(**model_inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
