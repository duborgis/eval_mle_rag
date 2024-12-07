TOKEN_INFERENCE ?= TOKEN_INFERENCE
TOKEN_VECTOR ?= TOKEN_VECTOR

ruff-install:
	@curl -LsSf https://astral.sh/ruff/install.sh | sh

ruff-utils:
	@ruff check utils

ruff-llm:
	@ruff check llm_api_service

ruff-vector:
	@ruff check load_vector_service

ruff-all:
	@ruff check .

install-requirements:
	@uv pip install -r ./utils/requirements.txt
	@uv pip install -r ./llm_api_service/requirements.txt
	@uv pip install -r ./load_vector_service/requirements.txt

uv-install:
	@curl -LsSf https://astral.sh/uv/install.sh | sh


serve-vector:
	@cd load_vector_service && uvicorn src.main:app --host 0.0.0.0 --port 5002 --reload

serve-llm:
	@cd llm_api_service && uvicorn src.main:app --host 0.0.0.0 --port 5003 --reload

test-vector:
	@cd load_vector_service/src/modules/tests && pytest tests.py -s

test-llm:
	@cd llm_api_service/src/modules/tests && pytest tests.py -s

# comandos que serão utilizados pelo avaliador

up-n-wait:
	@make down
	@chmod +x ./run_n_wait.sh
	@./run_n_wait.sh gpu
	@nvidia-smi

up-n-wait-cpu:
	@make down
	@chmod +x ./run_n_wait.sh
	@./run_n_wait.sh cpu

create-vector:
	@chmod +x ./utils/load_n_vectorize_out.sh
	@cd ./utils && ./load_n_vectorize_out.sh


ask-script:
	@chmod +x ./avaliacao/ask_script.sh
	@cd ./avaliacao && ./ask_script.sh


vai-test:
	@make up-n-wait
	@make create-vector
	@make ask-script

vai-test-cpu:
	@make up-n-wait-cpu
	@make create-vector
	@make ask-script


extract-url:
	@curl -X POST http://localhost:5002/extract/extract-url -H "Content-Type: application/json" -d '{"url": "https://hotmart.com/pt-br/blog/como-funciona-hotmart"}'


down:
	@docker compose down