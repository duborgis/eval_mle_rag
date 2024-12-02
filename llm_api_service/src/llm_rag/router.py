from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .utils import generate_response
from ..utils import generic_error_handler



llm_router = APIRouter()

class LLMData(BaseModel):
    question: str
    title_rag: str



@llm_router.get("/health")
@generic_error_handler
async def health_route():
    return JSONResponse(content={"detail": "OK"}, status_code=status.HTTP_200_OK)


@llm_router.post("/generate-response")
@generic_error_handler
async def generate_response_route(data: LLMData):
    response = await generate_response(data.question, data.title_rag)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

