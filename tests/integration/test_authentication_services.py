import pytest

from library.authentication import services as services
from library.authentication.services import NameNotUniqueException, AuthenticationException


def test_add_user(in_memory_repo):
    username = 'abc123'
    password = 'abcABC123'

    services.add_user(username, password, in_memory_repo)
    user = services.get_user(username, in_memory_repo)
    user_as_dict = services.get_user(username, in_memory_repo)

    assert user_as_dict['user_name'] == username

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(NameNotUniqueException):
        services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(services.AuthenticationException):
        services.authenticate_user(new_user_name, '0987654321', in_memory_repo)

