from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.logger import logger


def custom_exception_handler(exc, context):
    """Глобальный обработчик исключений"""

    # Стандартная обработка DRF
    response = exception_handler(exc, context)

    if response is not None:
        return response

    # ValidationError -> 400
    if isinstance(exc, ValidationError):
        logger.warning(f"Validation error: {exc}")
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    # DoesNotExist -> 404
    if isinstance(exc, ObjectDoesNotExist):
        model_name = exc.__class__.__name__.replace("DoesNotExist", "")
        logger.warning(f"{model_name} not found")
        return Response({"error": f"{model_name} not found"}, status=status.HTTP_404_NOT_FOUND)

    # IntegrityError -> 400
    if isinstance(exc, IntegrityError):
        logger.warning(f"Integrity error: {exc}")
        return Response(
            {"error": "Duplicate entry or integrity violation"}, status=status.HTTP_400_BAD_REQUEST
        )

    # ValueError -> 400
    if isinstance(exc, ValueError):
        logger.warning(f"Value error: {exc}")
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    # Все остальные ошибки -> 500
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response(
        {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
