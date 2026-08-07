from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.logger import logger


def custom_exception_handler(exc, context):
    """Кастомный обработчик исключений для DRF"""
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return Response(
            {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    logger.error(f"API Error: {exc}")
    return response
