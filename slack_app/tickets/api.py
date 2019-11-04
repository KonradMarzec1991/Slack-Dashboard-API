from rest_framework import viewsets
from .serializers import TicketSerializer
from .models import Ticket


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()