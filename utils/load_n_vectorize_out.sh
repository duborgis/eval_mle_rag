#!/bin/bash

# Configuração dos campos do form-data
TITLE="O que é Hotmart e como funciona? DESCUBRA TUDO!"
DESCRIPTION="testando nosso rag"
USER_ID="VAR_TEST_ONLY"
URL="https://hotmart.com/pt-br/blog/como-funciona-hotmart"
FILE="./out/output.txt"

# Faz a requisição POST usando curl com form-data
curl -s -X POST \
  -F "title=$TITLE" \
  -F "description=$DESCRIPTION" \
  -F "user_id=$USER_ID" \
  -F "url=$URL" \
  -F "file=@$FILE" \
  http://localhost:5002/vector/text-to-vector