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

    lookup_field = 'key'
    permission_classes = ()

    def list(self, request):
        return Response(status_dict())

    def retrieve(self, request, key):
        if not is_status_attr_public(key):
            raise Http404
        return Response(status_dict(key))