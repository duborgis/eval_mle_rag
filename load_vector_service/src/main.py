from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .configs import VERSION
from .ingest_vec.router import vector_router
from .utils import config_logging

config_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
# app.add_middleware(AuthenticationMiddleware)

@app.get('/')
def health_check():
    return JSONResponse(    
        content=f'Vector API - Backend {VERSION}',
        status_code=status.HTTP_200_OK
    )

app.include_router(vector_router, prefix='/vector')

