from fastapi import Request
from fastapi.responses import JSONResponse

from backend.utils.exceptions import CodeUnderstandingError


async def error_handler(request: Request, exc: CodeUnderstandingError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
