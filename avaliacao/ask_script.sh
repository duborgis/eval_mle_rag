#!/bin/bash

# Lê cada linha do arquivo perguntas.txt
while IFS= read -r pergunta; do
    # Cria o JSON para a requisição
    json_data="{
        \"question\": \"$pergunta\",
        \"title_rag\": \"O que é Hotmart e como funciona? DESCUBRA TUDO!\"
    }"
    
    echo "P: $pergunta"
    echo -n "R: "
    
    # Faz a requisição POST e extrai apenas o campo "response" do JSON retornado
    # -s silencia o output do progresso do curl
    curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$json_data" \
        http://192.168.1.102:5003/llm/generate-response | jq -r '.response'
    
    # Opcional: adiciona um delay entre as requisições
    sleep 1
    
    echo "-------------------"
done < perguntas.txt