"""
API views
"""

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


class SingleTicketViewSet(viewsets.ModelViewSet):
    """
    View without filtering system
    """
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    """
    Ticket modelSetView, two methods are overwritten:

    1) get_queryset - returns qs filtered with url params
    2) list - delivers two hierarchies:
        a) filtered qs with tickets
        b) workspace / channel hierarchy
    """
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

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
            workspace,
            channels,
            q,
            status,
            severity
        )

    def list(self, request, *args, **kwargs):
        """
        Returns serialized tickets and workspace hierarchy
        """
        qs = TicketSerializer(self.get_queryset(), many=True).data
        wk_list = Ticket.objects.get_workspace_hierarchy()

        resp = {
            'list': qs,
            'workspace': wk_list
        }
        return Response(resp)


class NamespaceViewSet(viewsets.ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = Namespace.objects.all()