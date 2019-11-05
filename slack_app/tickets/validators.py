from django.core.validators import ValidationError


def validate_data(value):
    if value is None or value == {}:
        raise ValidationError('Data cannot be empty or null')
    try:
        workspace = value['workspace']
        channel = value['channel']
    except KeyError:
        raise ValidationError('Workspace or channel not provided')
