from functools import wraps
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from logging.handlers import RotatingFileHandler
from .configs import LOG_LEVEL, HS256_PASSWORD
import jwt  # Add this import
import asyncio

def generic_error_handler(func):
    @wraps(func)
    async def handler(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(
                content={'error': f'{e}'},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return handler

def verify_access_token(request):
    try:
        token = request.headers.get('authorization').replace('Bearer ', '')
        payload = jwt.decode(token, HS256_PASSWORD, algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error: {str(e)}")

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS":
            response = JSONResponse(status_code=200, content='{"detail": "OK"}')
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response
        try:
            verify_access_token(request)
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

def config_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler("src/backend.log", maxBytes=1048576, backupCount=5),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)