from math import ceil
from typing import Any

from rest_framework.pagination import PageNumberPagination

from helpers.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        page_size: int | Any = self.get_page_size(self.request) if self.request else 0
        data_count = self.page.paginator.count if self.page else 0

        return Response({
            'pagination': True,
            'paginated_data': data,
            'meta': {
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
                'page_current': self.page.number if self.page else 0,
                'page_total': ceil(data_count / page_size),
                'page_size': page_size,
                'data_count': data_count,
            }
        })
