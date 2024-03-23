import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import status

from repair_core.models import RepairMan
from repair_core.signals import handlers


User = get_user_model()


@pytest.fixture(name='get_permissions')
def fixture_get_permissions():
    """A list of permissions strings to use with .has_perms() method."""
    perm_queryset = Permission.objects.filter(
        codename__in=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
    )

    permissions = [
        f"{perm.content_type.app_label}.{perm.codename}" for perm in perm_queryset
    ]

    return permissions


@pytest.fixture(name='create_user_instance')
def fixture_create_user_instance():
    """Create and return a User instance."""
    return User.objects.create_user(
        username='repairman',
        password='Ab1_Fr2S$',
        email='repairman@local.host',
    )


@pytest.fixture(name='create_repairman_instance')
def fixture_create_repairman_instance(create_user_instance):
    """Create and return a RepairMan instance."""
    def _create_repairman_instance(phone='1'):
        return RepairMan.objects.create(user=create_user_instance, phone=phone)
    return _create_repairman_instance


@pytest.fixture(name='get_repairmen_list')
def fixture_get_repairmen_list(api_client):
    """Perform HTTP GET request on /core/repairmen/ API endpoint."""
    def _get_repairmen_list():
        return api_client.get('/core/repairmen/')
    return _get_repairmen_list


@pytest.fixture(name='create_repairman')
def fixture_create_repairman(api_client):
    """Perform HTTP POST request on /core/repairmen/ API endpoint."""
    def _create_repairman(data):
        return api_client.post('/core/repairmen/', data, format='json')
    return _create_repairman


@pytest.fixture(name='retrieve_repairman')
def fixture_retrieve_repairman(api_client):
    """Retrieves a specific repairman using /core/repairmen/{repairman_id}/ endpoint"""
    def _retrieve_repairman(repairman_id: int):
        return api_client.get(f"/core/repairmen/{repairman_id}/")
    return _retrieve_repairman


@pytest.fixture(name='delete_repairman')
def fixture_delete_repairman(api_client):
    """Performs a HTTP DELETE request on /core/repairmen/{repairman_id}/ endpoint"""
    def _delete_repairman(repairman_id: int):
        return api_client.delete(f"/core/repairmen/{repairman_id}/")
    return _delete_repairman


@pytest.mark.django_db
class TestRepairManSignals:
    """Test the signals associated to a RepairMan model."""

    def test_if_user_has_right_perms_after_repairman_creation(self, get_permissions, create_user_instance):
        """Test if an associated User to a RepairMan has the right permissions after creation."""
        user = create_user_instance
        RepairMan.objects.create(user=user, phone='1')
        # https://docs.djangoproject.com/en/5.0/ref/models/instances/#refreshing-objects-from-database
        user.refresh_from_db()

        # https://docs.pytest.org/en/latest/how-to/assert.html
        assert user.is_staff, 'Assert that the user is a staff member'
        # https://docs.djangoproject.com/en/5.0/ref/contrib/auth/#django.contrib.auth.models.User.has_perms
        assert user.has_perms(get_permissions), \
            'Assert that the user has the necessary permissions for the RepairMan role.'

    def test_if_repairman_deletion_revokes_user_perms(self, get_permissions, create_user_instance):
        """Test if deleting a RepairMan instance revokes the associated user's permissions."""
        user = create_user_instance
        repairman = RepairMan.objects.create(user=user, phone='1')
        repairman.delete()
        user.refresh_from_db()

        assert user.is_staff is False, 'Assert that the user is not a staff member.'
        assert user.has_perms(get_permissions) is False, \
            'Assert that the user does not have the permissions required for the RepairMan role.'


@pytest.mark.django_db
class TestListRepairMen:
    """Test the /core/repairmen/ API endpoint listing functionality."""

    def test_if_anonymous_user_get_request_returns_401(self, get_repairmen_list):
        """Test if anonymous user GET HTTP request returns a 401 status"""
        response = get_repairmen_list()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot list the repairmen'

    def test_if_authenticated_user_get_request_returns_403(self, authenticate, get_repairmen_list):
        """Test if authenticated user GET HTTP request returns a 403 status"""
        authenticate()
        response = get_repairmen_list()

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot list the repairmen'

    def test_if_staff_user_get_request_returns_200(self, authenticate, get_repairmen_list):
        """Test if staff user GET HTTP request returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
        )
        response = get_repairmen_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user with right permissions can list the repairmen'

    def test_if_superuser_get_request_returns_200(self, authenticate, get_repairmen_list):
        """Test if superuser GET HTTP request returns a 200 status"""
        authenticate(is_superuser=True)
        response = get_repairmen_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can list the repairmen'


@pytest.mark.django_db
class TestRetrieveRepairMan:
    """Test the /core/repairmen/{repairman_id}/ API endpoint retrieving functionality."""

    def test_if_anonymous_user_retrieve_returns_401(self, create_repairman_instance, retrieve_repairman):
        """Test if anonymous user retrieve returns a 401 status"""
        repairman = create_repairman_instance()

        response = retrieve_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot retrieve a repairman'

    def test_if_authenticated_user_retrieve_returns_403(self, create_repairman_instance,
                                                        authenticate, retrieve_repairman):
        """Test if authenticated user retrieve returns a 403 status"""
        authenticate()
        repairman = create_repairman_instance()

        response = retrieve_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot retrieve a repairman'

    def test_if_staff_user_retrieve_returns_200(self, create_repairman_instance,
                                                authenticate, retrieve_repairman):
        """Test if staff user retrieve returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
        )
        repairman = create_repairman_instance()

        response = retrieve_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user can retrieve a specific repairman'
        assert {'id': response.data['id'], 'phone': response.data['phone']} == \
            {'id': repairman.id, 'phone': repairman.phone}, \
            'Assert that both database and response information about a repairman are equal'

    def test_if_superuser_retrieve_returns_200(self, create_repairman_instance,
                                               authenticate, retrieve_repairman):
        """Test if superuser retrieve returns a 200 status"""
        authenticate(is_superuser=True)
        repairman = create_repairman_instance()

        response = retrieve_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can retrieve a specific repairman'
        assert {'id': response.data['id'], 'phone': response.data['phone']} == \
            {'id': repairman.id, 'phone': repairman.phone}, \
            'Assert that both database and response information about a repairman are equal'


@pytest.mark.django_db
class TestDeleteRepairMan:
    """Test the /core/repairmen/{repairman_id} API endpoint deleting functionality."""

    def test_if_anonymous_user_delete_returns_401(self, create_repairman_instance, delete_repairman):
        """Test if anonymous user delete returns a 401 status"""
        repairman = create_repairman_instance()

        response = delete_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot delete a repairman'

    def test_if_authenticated_user_delete_returns_403(self, create_repairman_instance,
                                                      authenticate, delete_repairman):
        """Test if authenticated user delete returns a 403 status"""
        authenticate()
        repairman = create_repairman_instance()

        response = delete_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot delete a repairman'

    def test_if_staff_user_delete_returns_403(self, create_repairman_instance,
                                              authenticate, delete_repairman):
        """Test if staff user delete returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
        )
        repairman = create_repairman_instance()

        response = delete_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot delete a repairman'

    def test_if_superuser_delete_returns_204(self, create_repairman_instance,
                                             authenticate, delete_repairman):
        """Test if superuser delete returns a 204 status"""
        authenticate(is_superuser=True)
        repairman = create_repairman_instance()

        response = delete_repairman(repairman_id=repairman.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT, \
            'Assert that a superuser can delete a specific repairman'


@pytest.mark.django_db
class TestCreateRepairMan:
    """Test creating a new RepairMan using the /core/repairmen/ API endpoint."""

    def test_if_anonymous_user_create_returns_401(self, create_user_instance, create_repairman):
        """Test if anonymous user create returns a 401 status"""
        user = create_user_instance
        data = {
            'user_id': user.id,
            'phone': '1'
        }

        response = create_repairman(data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot create a new repairman'

    def test_if_authenticated_user_create_returns_403(self, create_user_instance,
                                                      authenticate, create_repairman):
        """Test if authenticated user create returns a 403 status"""
        authenticate()
        user = create_user_instance
        data = {
            'user_id': user.id,
            'phone': '1'
        }

        response = create_repairman(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot create a new repairman'

    def test_if_staff_user_create_returns_403(self, create_user_instance,
                                              authenticate, create_repairman):
        """Test if staff user create returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
        )
        user = create_user_instance
        data = {
            'user_id': user.id,
            'phone': '1'
        }

        response = create_repairman(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot create a new repairman'

    def test_if_superuser_create_returns_201(self, create_user_instance,
                                             authenticate, create_repairman):
        """Test if superuser create returns a 201 status"""
        authenticate(is_superuser=True)
        user = create_user_instance
        data = {
            'user_id': user.id,
            'phone': '1'
        }

        response = create_repairman(data)

        assert response.status_code == status.HTTP_201_CREATED, \
            'Assert that a superuser can create a new repairman using the API'
        assert response.data['id'] > 0, 'Assert that the repairman id is present in response body'
        assert response.data['phone'] == data['phone']
