import asyncio
from functools import wraps
from fastapi import status
from fastapi.responses import JSONResponse
import logging
from logging.handlers import RotatingFileHandler
from ..configs import LOG_LEVEL


def generic_error_handler(func):
    @wraps(func)
    async def handler(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(
                content={"error": f"{e}"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return handler


def config_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler("src/backend.log", maxBytes=1048576, backupCount=5),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
