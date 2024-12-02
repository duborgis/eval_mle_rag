from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .utils import extract_content_from_webpage
from ..utils import generic_error_handler

extract_url_router = APIRouter()


class ExtractUrlData(BaseModel):
    url: str

@extract_url_router.post("/extract-url")
@generic_error_handler
def extract_url(data: ExtractUrlData):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "URL extraída com sucesso", "content": extract_content_from_webpage(data.url)})
