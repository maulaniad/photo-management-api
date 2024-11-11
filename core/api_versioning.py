from django.conf import settings
from rest_framework.versioning import BaseVersioning
from rest_framework.request import Request


class APIVersioning(BaseVersioning):
    def determine_version(self, request: Request, *args, **kwargs):
        default_version = settings.REST_FRAMEWORK['DEFAULT_VERSION']
        return request.META.get('HTTP_X_API_VERSION', default_version)
