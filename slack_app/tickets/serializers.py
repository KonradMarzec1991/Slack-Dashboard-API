from rest_framework import serializers
from .models import Ticket, Namespace


class TicketSerializer(serializers.ModelSerializer):
    namespace = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Namespace.objects.all()
    )

    class Meta:
        model = Ticket
        fields = [
            'title', 'description', 'status', 'severity', 'reporter', 'namespace'
        ]

