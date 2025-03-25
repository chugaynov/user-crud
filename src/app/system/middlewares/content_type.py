from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ContentTypeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if not response.headers.get("Content-Type"):
            response.headers["Content-Type"] = "application/json"
        return response