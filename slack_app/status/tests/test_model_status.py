import pytest
from django.test import override_settings

from status.models import (
    Status,
    is_status_attr_public,
    status_dict
)


@pytest.fixture
def sample_status():
    return Status()


@override_settings(VERSION='1.0.0', COMMIT='27836#4jnf')
def test_status_attrs(sample_status):
    assert sample_status.commit == '27836#4jnf'
    assert sample_status.version == '1.0.0'


def test_correct_attrs():
    assert is_status_attr_public('commit') is True
    assert is_status_attr_public('_wrong') is False
    assert is_status_attr_public('version') is True
    assert is_status_attr_public('correct') is False


def test_status_dict_correct_key():
    status = status_dict('commit')
    assert status['commit'] == '2874#952'
    assert len(status) == 1
    status = status_dict()
    assert status['version'] == '1.0.0'
    assert len(status) == 2  # both version and commit are there


def test_status_dict_wrong_key():
    with pytest.raises(AttributeError):
        status_dict('_wrong')


