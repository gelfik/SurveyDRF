from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param
from urllib import parse
from django.utils.encoding import force_str

class Pagination(PageNumberPagination):
    page_size = 20
    max_page_size = 1000

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(self.request.build_absolute_uri()))
        return replace_query_param(f'?{query}', self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(self.request.build_absolute_uri()))
        return replace_query_param(f'?{query}', self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'curent': self.page.number,
            'count': self.page.paginator.num_pages,
            'results': data
        })
