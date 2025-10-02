import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger
import json

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        body = await request.body()
        try:
            body_str = body.decode('utf-8')
            if body_str:
                body_json = json.loads(body_str)
                logger.info(f"Request: {request.method} {request.url} - Payload: {body_json}")
            else:
                logger.info(f"Request: {request.method} {request.url}")
        except:
            logger.info(f"Request: {request.method} {request.url} - Body: {body[:100]}...")
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {response.status_code} - Time: {process_time:.2f}s")
        
        return response