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
    def get_filtered_qs(self,
                        workspace=None,
                        channel=None,
                        q=None,
                        status=None,
                        severity=None,
                        namespace_id=None):
        qs = self.get_queryset()

        if namespace_id:
            qs = qs.filter(namespace_id=namespace_id)
        if workspace:
            qs = qs.filter(data__workspace=workspace)
        if channel:
            channel = channel.split(',')
            qs = qs.filter(data__channel_in=channel)
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if severity:
            qs = qs.filter(severity=severity)
        return qs

    def get_one_column_data(self, col_name):
        return self.get_queryset().values_list(col_name, flat=True)

    def get_workspace_hierarchy(self):
        qs = self.get_one_column_data('data')

        workspace_list = dict()

        for item in qs:
            workspace = item['workspace']
            channel = item['channel']

            if workspace not in workspace_list:
                workspace_list[workspace] = []
            if channel not in workspace_list[workspace]:
                workspace_list[workspace].append(channel)

        return workspace_list


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

    namespace_id = models.ForeignKey(
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
