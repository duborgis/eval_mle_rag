import re
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")


# é preciso tomar muito cuidado com o uso dessa função, pois ela é responsável
# por limpar o texto para que o modelo de embeddings consiga entender o contexto
# mas em varios casos, conforme comentado abaixo, PERDEMOS O CONTEXTO
# importante verificar se o contexto está sendo preservado
def normalize_chunk(text: str):
    # Remove espaços em branco no início e fim do texto
    text = text.strip()
    print(f"Strip: {text}\n")

    # Remove todos os caracteres que não são palavras ou espaços
    # Ex: pontuação, símbolos especiais, etc.
    # Pro caso de R$ pode ser ruim, pois o R$ é um símbolo monetário
    # O caso da % pode ser ruim, pois é um símbolo de porcentagem
    text = re.sub(r"[^\w\s]", "", text)
    print(f"Regex pontuação e símbolos: {text}\n")
    # Converte todo o texto para minúsculo
    # Ex: "Olá Mundo" -> "olá mundo"
    text = text.lower()
    print(f"Lower: {text}\n")
    # Remove todos os caracteres que não são letras do alfabeto ou espaços
    # Ex: remove números e outros caracteres especiais que sobraram
    # Muito ruim pois a primeira pergunta sobre "10% do valor do produto"
    # Vai ficar "valor do produto", perdemos o contexto e foi por isso que o RAG
    # perdeu a capacidade de responder a primeira pergunta ->Qual é a taxa cobrada pela Hotmart por venda para produtos acima de R$10 no Brasil?
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    print(f"Regex letras apenas: {text}\n")

    # Remove stopwords do português (palavras muito comuns que geralmente não agregam significado)
    # Ex: "o", "a", "para", "com", etc.
    stop_words = set(stopwords.words("portuguese"))
    text = " ".join([word for word in text.split() if word not in stop_words])
    print(f"Stopwords removidas: {text}\n")

    return text


if __name__ == "__main__":
    word = (
        "O PREÇO é R$ 1.250,00 + 10% de taxa p/ cada PRODUTO! (válido até 25/12/2023)"
    )
    print(f"Original: {word}\n")
    text = normalize_chunk(word)
    print(f"Normalizado: {text}\n")


# Original: O PREÇO é R$ 1.250,00 + 10% de taxa p/ cada PRODUTO! (válido até 25/12/2023)

# Strip: O PREÇO é R$ 1.250,00 + 10% de taxa p/ cada PRODUTO! (válido até 25/12/2023)

# Regex pontuação e símbolos: O PREÇO é R 125000  10 de taxa p cada PRODUTO válido até 25122023

# Lower: o preço é r 125000  10 de taxa p cada produto válido até 25122023

# Regex letras apenas: o preo  r    de taxa p cada produto vlido at

# Stopwords removidas: preo r taxa p cada produto vlido at

# Normalizado: preo r taxa p cada produto vlido at
