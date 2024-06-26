import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


# Get the default user model.
User = get_user_model()


@pytest.fixture(name='api_client')
def fixture_api_client():
    """Returns a new APIClient object"""
    return APIClient()


@pytest.fixture(name='authenticate')
def fixture_authenticate(api_client):
    """
    Keyword Arguments:
    set `is_staff` to True for an authenticated staff user.
    set `is_superuser` to True for an authenticated superuser.
    set `permissions` to a list of permission codenames.
    """
    def do_authenticate(is_staff=False, is_superuser=False, permissions=None):
        user = User.objects.create(
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        if permissions:
            permissions = Permission.objects.filter(
                codename__in=permissions
            )
            user.user_permissions.set(permissions)

        return api_client.force_authenticate(user=user)

    return do_authenticate
