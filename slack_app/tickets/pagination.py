"""
Ticket API pagination
"""

from rest_framework import pagination


class TicketPagination(pagination.PageNumberPagination):

    page_size = 10
    page_size_query_param = 'p'