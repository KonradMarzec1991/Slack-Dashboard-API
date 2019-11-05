from django.db import models
from django.contrib.postgres.fields import JSONField

from .validators import validate_data


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
        choices=STATUS)
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY)
    reporter = models.CharField(max_length=25)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = JSONField(
        default=dict,
        validators=[validate_data])

    def __str__(self):
        return f'{self.title} of {self.reporter}'


class Namespace(models.Model):

    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f'{self.name}'
