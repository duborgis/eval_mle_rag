from fastapi import APIRouter, status, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .utils import create_and_store_embeddings, retrieve_similar_data
from ..utils import generic_error_handler

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
        url: str = Form(...)
    ):
        return cls(
            title=title,
            description=description,
            user_id=user_id,
            url=url
        )

class VectorizeAskData(BaseModel):
    question: str
    collection_name: str
    @classmethod
    def as_form(
        cls,
        question: str = Form(...),
        collection_name: str = Form(...)
    ):
        return cls(
            question=question,
            collection_name=collection_name
        )


@vector_router.post("/text-to-vector")
@generic_error_handler
async def text_to_vector(
    data: TextToVectorData = Depends(TextToVectorData.as_form),
    file: UploadFile = File(...)
):
    text_content = await file.read()
    text_str = text_content.decode('utf-8')

    collection_name = data.title
    
    create_and_store_embeddings(
        texts=text_str,
        collection_name=collection_name
    )

    return JSONResponse(content={"detail": "OK"}, status_code=status.HTTP_200_OK)

@vector_router.post("/vectorize-ask")
@generic_error_handler
async def vectorize_ask(
    data: VectorizeAskData = Depends(VectorizeAskData.as_form)
):
    print(data)
    try:
        search_result = retrieve_similar_data(data.question, data.collection_name)
        return JSONResponse(content={"detail": search_result}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content={"detail": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)