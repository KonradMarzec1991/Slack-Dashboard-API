"""
Tickets API pagination
"""

from rest_framework import pagination
from rest_framework.response import Response


class TicketPagination(pagination.PageNumberPagination):

    page_size = 5
    page_query_param = 'p'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'num_of_tickets': self.page.paginator.count,
            'current_page': self.page.number,
            'num_of_pages': self.page.paginator.num_pages,
            'tickets': data
        })
