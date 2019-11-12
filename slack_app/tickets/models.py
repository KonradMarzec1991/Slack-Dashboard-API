"""
Tickets and namespace models with managers
"""

from django.db.models import Q

from django.db import models
from django.contrib.postgres.fields import JSONField

from .validators import (
    validate_data,
    validate_status,
    validate_severity,
)


class TicketManager(models.Manager):
    """
    Manager delivers two methods:
        1) filter by params required in Ticket modelViewSet - see views.py
        2) Workspace and channel hierarchy - dictionary of workspaces with
        unique channels within
    """
    def get_filtered_qs(self, workspace=None, channels=None, q=None, status=None, severity=None):
        qs = self.get_queryset()

        if workspace:
            qs = qs.filter(data__workspace=workspace)
        if channels:
            channels = channels.split(',')
            qs = qs.filter(data__channels_in=channels)
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if severity:
            qs = qs.filter(severity=severity)
        return qs


class Ticket(models.Model):

    NOT_STARTED = 'not started'
    DOING = 'doing'
    DONE = 'done'

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    STATUS = (
        (NOT_STARTED, 'not started'),
        (DOING, 'doing'),
        (DONE, 'done'),
    )

    SEVERITY = (
        (LOW, 'low'),
        (MEDIUM, 'medium'),
        (HIGH, 'high')
    )

    namespace = models.ForeignKey(
        'Namespace',
        on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    description = models.TextField()

    status = models.CharField(
        max_length=12,
        choices=STATUS,
        validators=[validate_status])

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY,
        validators=[validate_severity])

    reporter = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = JSONField(
        default=dict,
        validators=[validate_data])

    objects = TicketManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} of {self.reporter}'


class Namespace(models.Model):

    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f'{self.name}'
