"""
Status API viewset
"""

from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from .models import (
    status_dict,
    is_status_attr_public
)


class StatusViewSet(ViewSet):
    """
    Get a mapping from status keys (strings) to their values
    (may be different types).

    Provide a key in the URL after slash to GET a mapping
    containing only that specific key and its value
    """

    lookup_field = 'key'
    permission_classes = ()

    def list(self, request):
        # pylint: disable=unused-argument,no-self-use
        return Response(status_dict())

    def retrieve(self, request, key):
        # pylint: disable=unused-argument,no-self-use
        if not is_status_attr_public(key):
            raise Http404
        return Response(status_dict(key))