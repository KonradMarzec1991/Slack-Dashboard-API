"""
Model validators for status, severity and JSON fields
"""

from django.core.validators import ValidationError


def is_none_or_not_in(param, attributes=None):
    """
    Checks if model field value is None or is not in given list
    :param param: field value
    :param attributes: given list
    :return: boolean value
    """
    if attributes is None:
        return param is None
    return param is None or param not in attributes


def validate_data(value):
    if is_none_or_not_in(value) or value == {}:
        raise ValidationError('Data cannot be empty or null')
    try:
        workspace = value['workspace']
        channel = value['channel']
    except KeyError:
        raise ValidationError('Workspace or channel not provided')


def validate_status(status):
    if is_none_or_not_in(status, ['not started', 'doing', 'done']):
        raise ValidationError(
            'Status can be set to one of ("not started", "doing", "done")'
        )


def validate_severity(severity):
    if is_none_or_not_in(severity, ['low', 'medium', 'high']):
        raise ValidationError(
            'Status can be set to one of ("low", "medium", "high")'
        )
