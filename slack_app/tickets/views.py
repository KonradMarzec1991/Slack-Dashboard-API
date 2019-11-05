from rest_framework import viewsets
from .serializers import TicketSerializer, NamespaceSerializer
from .models import Ticket, Namespace


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class NamespaceViewSet(viewsets.ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = Namespace.objects.all()