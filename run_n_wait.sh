#!/bin/bash

MODE=$1

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para verificar se um serviço está respondendo, pois demora o download do modelo na primeira vez
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=300  # 15 minutos (300 * 5s)
    local attempt=1

    echo "Verificando disponibilidade do $service_name..."
    echo "URL: $url"
    echo -e "${YELLOW}Esse processo pode demorar, pois precisamos baixar e/ou carregar o modelo de LLM${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null; then
            echo -e "${GREEN}$service_name está pronto!${NC}"
            return 0
        fi
        echo "Tentativa $attempt de $max_attempts - $service_name ainda não está pronto... Aguarde!"
        attempt=$((attempt + 1))
        sleep 5
    done

    echo -e "${RED}Timeout esperando $service_name ficar disponível${NC}"
    return 1
}

# Inicia a stack
echo "Iniciando a stack Docker..."

if [ "$MODE" == "gpu" ]; then
    docker-compose up -d --build 
else
    docker-compose -f docker-compose-cpu.yaml up -d --build 
fi

# Verifica os serviços
check_service "load_vector_service" "http://localhost:5002/" || exit 1
check_service "llm_api_service" "http://localhost:5003/" || exit 1

# Faz a requisição GET e extrai apenas os nomes dos modelos
echo "Modelo disponível:"
echo "-------------------"
curl -s http://localhost:11434/api/tags | jq -r '.models[].name'

echo -e "${GREEN}Todos os serviços estão prontos!${NC}"

