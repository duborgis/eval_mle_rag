from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .configs import VERSION
from .routes.ingest import vector_router
from .utils.logging import config_logging
from .routes.extract import extract_url_router

config_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
# app.add_middleware(AuthenticationMiddleware)


@app.get("/")
def health_check():
    return JSONResponse(
        content=f"Vector API - Backend {VERSION}", status_code=status.HTTP_200_OK
    )


app.include_router(vector_router, prefix="/vector")
app.include_router(extract_url_router, prefix="/extract")
