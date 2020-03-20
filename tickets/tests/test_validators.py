import pytest

from django.core.exceptions import ValidationError

from tickets.validators import (
    is_none_or_not_in,
    validate_data,
    validate_status
)


def test_is_none_or_not_in():
    assert is_none_or_not_in(None) is True
    assert is_none_or_not_in('a', ['a', 'b']) is False


def test_validate_none():
    with pytest.raises(ValidationError):
        validate_data(None)
        validate_data({})

    item = dict(workspaces={})
    with pytest.raises(ValidationError):
        validate_data(item)


def test_validate_status():
    with pytest.raises(ValidationError):
        validate_status('aaaa')
        validate_status(None)




