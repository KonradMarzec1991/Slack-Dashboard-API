"""
Status API
"""

from django.conf import settings


class Status:
    """
    Keeps global API properties to be displayed under an URL
    """

    @property
    def commit(self):
        return getattr(settings, 'COMMIT')

    @property
    def version(self):
        return getattr(settings, 'VERSION')


def is_status_attr_public(attr):
    """
    :param attr: name of class attribute
    :return: if attr is public (bool value)
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






