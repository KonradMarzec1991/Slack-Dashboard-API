"""
Status API
"""

from django.conf import settings


class ApiStatus:
    """
    Class Status delivers API status/version
    """

    @property
    def status(self):
        return getattr(settings, 'status')

    @property
    def version(self):
        return getattr(settings, 'version')


def get_status_attributes():
    pass






