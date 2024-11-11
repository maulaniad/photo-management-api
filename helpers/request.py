from typing import Any, Union

from django.http import QueryDict
from rest_framework.request import Request as _Req


def _user_model_():
    from database.models import User
    return User


class Request(_Req):
    """
    Custom Request class to help with type annotations which was absent in rest_framework.
    """

    @property
    def data(self) -> Union[dict[str, Any], QueryDict]:
        current_data: dict[str, Any] | QueryDict = super().data  # type: ignore
        return current_data

    @property
    def user(self):
        return _user_model_()
