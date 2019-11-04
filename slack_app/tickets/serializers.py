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
            'id', 'title', 'description', 'status', 'severity', 'reporter', 'namespace'
        ]
        extra_kwargs = {
            'status': {
                'help_text': "Status might be only one of not started / doing / done"
            },
            'severity': {
                'help_text': "Severity might be only one of low / medium / high"
            }
        }


class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = ['name']

