from typing import Any, Iterable

from django.http import JsonResponse
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse
from rest_framework.exceptions import (MethodNotAllowed,
                                       NotAcceptable,
                                       NotFound,
                                       AuthenticationFailed,
                                       PermissionDenied,
                                       ValidationError,
                                       UnsupportedMediaType,
                                       Throttled,
                                       APIException)


class StandardExceptionFormatter(ExceptionFormatter):
    """
    Custom Standardized Response formatter.
    """

    def format_error_response(self, error_response: ErrorResponse):
        """Beautify the error response."""

        e = error_response.errors[0]
        e_detail = f"{e.detail.strip('.')}"
        e_attribute = f": {e.attr}" if e.attr else ""

        return {
            'status': self.exc.status_code,
            'success': False,
            'message': f"{e_detail}{e_attribute}",
            'error': error_response.type,
        }


class HttpError:
    """
    Custom HTTP error class to be raised on which will be caught by Standardized Response.
    """
    @staticmethod
    def _400_(detail: Iterable[Any] | str):
        return ValidationError(detail)

    @staticmethod
    def _401_(detail: Iterable[Any] | str):
        return AuthenticationFailed(detail)

    @staticmethod
    def _403_(detail: Iterable[Any] | str):
        return PermissionDenied(detail)

    @staticmethod
    def _404_(detail: Iterable[Any] | str):
        return NotFound(detail)

    @staticmethod
    def _405_(method: str, detail: Iterable[Any] | str):
        return MethodNotAllowed(method, detail)

    @staticmethod
    def _406_(detail: Iterable[Any] | str):
        return NotAcceptable(detail)

    @staticmethod
    def _415_(media_type: str, detail: Iterable[Any] | str):
        return UnsupportedMediaType(media_type, detail)

    @staticmethod
    def _429_(wait: float, detail: Iterable[Any] | str):
        return Throttled(wait, detail)

    @staticmethod
    def _500_(detail: Iterable[Any] | str):
        internal_server_error = APIException(detail)
        internal_server_error.status_code = 500
        internal_server_error.default_code = "internal_server_error"
        return internal_server_error


def handler_404(request, exception):
    return JsonResponse(
        {
            'status': 404,
            'success': False,
            'message': f"Resource {request.path} was not found on the server.",
            'error': "invalid_url",
        }, status=404
    )


def handler_500(request):
    return JsonResponse(
        {
            'status': 500,
            'success': False,
            'message': "Internal Server Error.",
            'error': "internal_server_error",
        }, status=500
    )
