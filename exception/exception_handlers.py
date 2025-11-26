import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from exception.app_exception import AppException

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    """添加全局异常处理器"""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """处理自定义应用异常"""
        logger.error(f"AppException: {exc.message}, Code: {exc.code}")

        return JSONResponse(
            status_code=exc.code,
            content={
                "code": -1,
                "message": exc.message,
                "detail": exc.detail,
                "data": None
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """处理HTTP异常"""
        logger.error(f"HTTPException: {exc.detail}, Status: {exc.status_code}")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": -1,
                "message": exc.detail,
                "data": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求验证异常"""
        logger.error(f"Validation error: {exc.errors()}")

        return JSONResponse(
            status_code=422,
            content={
                "code": -1,
                "message": "请求参数验证失败",
                "detail": exc.errors(),
                "data": None
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """处理未预期的全局异常"""
        logger.error(f"Global exception: {str(exc)}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "code": -1,
                "message": f"服务器内部错误:{str(exc)}",
                "data": None
            }
        )
