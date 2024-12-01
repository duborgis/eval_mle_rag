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

create-vector:
	@curl -X POST http://localhost:8000/create_vector \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer $(TOKEN_VECTOR)" \
		-d @utils/out/output.txt
