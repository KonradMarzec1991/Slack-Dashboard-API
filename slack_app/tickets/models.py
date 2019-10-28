from django.db import models
from django.contrib.postgres.fields import JSONField


class Ticket(models.Model):

    STATUS = (
        ('not started', 'not started'),
        ('doing', 'doing'),
        ('done', 'done'),
    )

    SEVERITY = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high')
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS)
    severity = models.CharField(max_length=10, choices=SEVERITY)
    reporter = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField(default={})

    def __str__(self):
        return f'{self.title} of {self.reporter}'
