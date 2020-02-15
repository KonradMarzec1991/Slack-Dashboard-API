# pylint: disable=no-member
from rest_framework import serializers
from .models import Ticket, Namespace


class TicketSerializer(serializers.ModelSerializer):
    namespace = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description',
            'status', 'severity', 'reporter',
            'data', 'namespace_id', 'namespace'
        ]
        extra_kwargs = {
            'status': {
                'help_text':
                    "Status might be only one of not started / doing / done"
            },
            'severity': {
                'help_text': "Severity might be only one of low / medium / high"
            },
            'data': {
                'help_text':
                    "Valid data json should contain workspace and channel"
            }
        }

    def get_namespace(self, obj):
        return obj.namespace_id.name


class NamespaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = ['id', 'name']

