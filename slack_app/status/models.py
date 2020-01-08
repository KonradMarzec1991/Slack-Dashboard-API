"""
Status API
"""

from django.conf import settings


class Status:
    """
    Class Status delivers API status/version
    """

    @property
    def status(self):
        return getattr(settings, 'COMMIT')

    @property
    def version(self):
        return getattr(settings, 'VERSION')


def is_status_attr_public(attr):
    """
    :param attr: name of class attribute
    :return: bool if attr is public
    """
    return not attr.startswith("_") and hasattr(Status, attr)


def status_dict(*attrs):
    """
    :return: dict with
        key - name of class attribute
        value - value of attribute
    """
    status = Status()
    if not attrs:
        attrs = (attr for attr in dir(status) if not attr.startswith("_"))
    return {attr: getattr(status, attr) for attr in attrs}






