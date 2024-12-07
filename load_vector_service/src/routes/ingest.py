from fastapi import APIRouter, status, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..utils.ingest import create_and_store_embeddings, retrieve_similar_data
from ..utils.logging import generic_error_handler
import sys
import os

vector_router = APIRouter()


class TextToVectorData(BaseModel):
    title: str
    description: str
    user_id: str
    url: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        user_id: str = Form(...),
        url: str = Form(...),
    ):
        return cls(title=title, description=description, user_id=user_id, url=url)


class VectorizeAskData(BaseModel):
    question: str
    collection_name: str

    @classmethod
    def as_form(cls, question: str = Form(...), collection_name: str = Form(...)):
        return cls(question=question, collection_name=collection_name)


@vector_router.post("/text-to-vector")
@generic_error_handler
async def text_to_vector(
    data: TextToVectorData = Depends(
        TextToVectorData.as_form
    ),  # as_form é necessário para que o FastAPI consiga lidar com o multipart/form-data
    file: UploadFile = File(...),
):
    try:
        text_content = await file.read()
        text_str = text_content.decode("utf-8")

        collection_name = data.title

        create_and_store_embeddings(texts=text_str, collection_name=collection_name)

        return JSONResponse(content={"detail": "OK"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@vector_router.post("/vectorize-ask")
@generic_error_handler
async def vectorize_ask(
    data: VectorizeAskData = Depends(
        VectorizeAskData.as_form
    ),  # Depends sistema de injeção de dependência
):
    print(data)
    try:
        search_result = retrieve_similar_data(data.question, data.collection_name)
        return JSONResponse(
            content={"detail": search_result}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
