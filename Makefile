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

up:
	@docker compose up -d --build 


down:
	@docker compose down


serve-vector:
	@cd load_vector_service && uvicorn src.main:app --host 0.0.0.0 --port 5002 --reload

serve-llm:
	@cd llm_api_service && uvicorn src.main:app --host 0.0.0.0 --port 5003 --reload

ask:
	@curl -X POST http://localhost:8000/ask \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer $(TOKEN_INFERENCE)" \
		-d '{"question": "O que é a Hotmart?"}'





up-n-wait:
	@chmod +x ./run_n_wait.sh
	@./run_n_wait.sh


create-vector:
	@chmod +x ./utils/load_n_vectorize_out.sh
	@cd ./utils && ./load_n_vectorize_out.sh


ask-script:
	@chmod +x ./avaliacao/ask_script.sh
	@cd ./avaliacao && ./ask_script.sh
