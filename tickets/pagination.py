"""
Tickets API pagination
"""

from rest_framework import pagination
from rest_framework.response import Response


class TicketPagination(pagination.PageNumberPagination):
    """
    Simple API pagination - delivers basic indicators:
    A) links - to next or previous page if exists else None
    B) num_of_tickets - total number of given users tickets
    C) current_page - active page
    D) num_of_pages - number of tickets / tickets per page (default: 10)
    E) tickets - tickets db data
    """

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
