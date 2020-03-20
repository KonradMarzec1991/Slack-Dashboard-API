# pylint: disable=no-member
"""
Main ticket API views for filtering and displaying all tickets in db
"""
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (
    TicketSerializer,
    NamespaceSerializer
)

from .models import (
    Ticket,
    Namespace
)

from .pagination import TicketPagination


def index(request):
    return render(request, 'index.html')


class SingleTicketViewSet(viewsets.ModelViewSet):
    # pylint: disable=too-many-ancestors
    """
    Ticket view without filtering functions
    """
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    # pylint: disable=too-many-ancestors
    """
    Ticket modelSetView, two methods are overwritten:

    1) get_queryset - returns qs filtered with url params
    2) list - delivers two hierarchies:
        a) filtered qs with tickets
        b) workspace / channel hierarchy
    """

    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    pagination_class = TicketPagination

    def get_queryset(self):
        """
        View method to return queryset filtered with url params
        :return: queryset filtered with url params
        """
        url_params = self.request.query_params

        q = url_params.get('q', None)

        status = url_params.get('status', None)
        severity = url_params.get('severity', None)

        workspace = url_params.get('workspace', None)
        channels = url_params.get('channel', None)

        return Ticket.objects.get_filtered_qs(
            workspace=workspace,
            channel=channels,
            q=q,
            status=status,
            severity=severity,
            namespace_id=self.kwargs['namespace_pk']
        )

    def list(self, request, *args, **kwargs):
        # pylint: disable=unused-argument
        """
        Returns serialized tickets and workspace hierarchy
        """
        qs = super(TicketViewSet, self).list(request)
        wk_list = Ticket.objects.get_workspace_hierarchy()

        resp = {
            'list': qs.data,
            'workspace': wk_list
        }
        return Response(resp)


class NamespaceViewSet(viewsets.ModelViewSet):
    """
    Basic viewset for class `Namespace`, looks up for namespace id
    """
    # pylint: disable=too-many-ancestors
    serializer_class = NamespaceSerializer
    queryset = Namespace.objects.all()

    lookup_field = 'pk'
