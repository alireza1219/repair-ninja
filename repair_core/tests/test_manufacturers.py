import pytest

from rest_framework import status

from repair_core.models import Manufacturer
from repair_core.permissions import REPAIRMAN_DEFAULT_PERMISSIONS


@pytest.fixture(name='create_manufacturer_instance')
def fixture_create_manufacturer_instance():
    """Create and return a Manufacturer instance."""
    def _create_manufacturer_instance(name='E Corp'):
        return Manufacturer.objects.create(name=name)
    return _create_manufacturer_instance


@pytest.fixture(name='get_manufacturers_list')
def fixture_get_manufacturers_list(api_client):
    """Perform HTTP GET request on /core/manufacturers/ API endpoint."""
    def _get_manufacturers_list():
        return api_client.get('/core/manufacturers/')
    return _get_manufacturers_list


@pytest.fixture(name='create_manufacturer')
def fixture_create_manufacturer(api_client):
    """Perform HTTP POST request on /core/manufacturers/ API endpoint."""
    def _create_manufacturer(data: dict):
        return api_client.post('/core/manufacturers/', data, format='json')
    return _create_manufacturer


@pytest.fixture(name='retrieve_manufacturer')
def fixture_retrieve_manufacturer(api_client):
    """Retrieve a specific manufacturer using /core/manufacturers/{manufacturer_id}/ endpoint."""
    def _retrieve_manufacturer(manufacturer_id: int):
        return api_client.get(f"/core/manufacturers/{manufacturer_id}/")
    return _retrieve_manufacturer


@pytest.fixture(name='update_manufacturer')
def fixture_update_manufacturer(api_client):
    """Perform HTTP PATCH request on /core/manufacturers/{manufacturer_id}/ endpoint."""
    def _update_manufacturer(manufacturer_id: int, data: dict):
        return api_client.patch(f"/core/manufacturers/{manufacturer_id}/", data, format='json')
    return _update_manufacturer


@pytest.fixture(name='delete_manufacturer')
def fixture_delete_manufacturer(api_client):
    """Perform HTTP DELETE request on /core/manufacturers/{manufacturer_id}/ endpoint."""
    def _delete_manufacturer(manufacturer_id: int):
        return api_client.delete(f"/core/manufacturers/{manufacturer_id}/")
    return _delete_manufacturer


@pytest.mark.django_db
class TestListManufacturers:
    """Test the /core/manufacturers/ API endpoint listing functionality."""

    def test_if_anonymous_user_get_request_returns_401(self, get_manufacturers_list):
        """Test if anonymous user GET HTTP request returns a 401 status"""
        response = get_manufacturers_list()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot list the manufacturers'

    def test_if_authenticated_user_get_request_returns_403(self, authenticate, get_manufacturers_list):
        """Test if authenticated user GET HTTP request returns a 403 status"""
        authenticate()

        response = get_manufacturers_list()

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot list the manufacturers'

    def test_if_staff_user_get_request_returns_200(self, authenticate, get_manufacturers_list):
        """Test if staff user GET HTTP request returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )

        response = get_manufacturers_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user can list the manufacturers'

    def test_if_superuser_get_request_returns_200(self, authenticate, get_manufacturers_list):
        """Test if superuser GET HTTP request returns a 200 status"""
        authenticate(is_superuser=True)

        response = get_manufacturers_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can list the manufacturers'


@pytest.mark.django_db
class TestCreateManufacturer:
    """Test creating a new manufacturer using the /core/manufacturers/ API endpoint."""

    def test_if_anonymous_user_create_returns_401(self, create_manufacturer):
        """Test if anonymous user create returns a 401 status"""
        data = {'name': 'E Corp'}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user can create a new manufacturer'

    def test_if_authenticated_user_create_returns_403(self, authenticate, create_manufacturer):
        """Test if authenticated user create returns a 403 status"""
        authenticate()
        data = {'name': 'E Corp'}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot create a new manufacturer'

    def test_if_staff_user_create_returns_201(self, authenticate, create_manufacturer):
        """Test if staff user create returns a 201 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        data = {'name': 'E Corp'}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_201_CREATED, \
            'Assert that an authenticated staff user can create a new manufacturer'
        assert response.data['id'] > 0, 'Assert that the manufacturer id is present in response body'
        assert response.data['name'] == data['name'], 'Assert the equality of names'

    def test_if_staff_user_create_using_invalid_data_returns_400(self,
                                                                 authenticate, create_manufacturer):
        """Test if staff user create using invalid data returns a 400 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        data = {}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            'Assert that a staff user cannot create a new manufacturer using invalid data'

    def test_if_superuser_create_returns_201(self, authenticate, create_manufacturer):
        """Test if superuser create returns a 201 status"""
        authenticate(is_superuser=True)
        data = {'name': 'E Corp'}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_201_CREATED, \
            'Assert that a superuser can create a new manufacturer using the API'
        assert response.data['id'] > 0, 'Assert that the manufacturer id is present in response body'
        assert response.data['name'] == data['name'], 'Assert the equality of names'

    def test_if_superuser_create_using_invalid_data_returns_400(self,
                                                                authenticate, create_manufacturer):
        """Test if superuser create using invalid data returns a 400 status"""
        authenticate(is_superuser=True)
        data = {}

        response = create_manufacturer(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            'Assert that a staff user cannot create a new manufacturer using invalid data'


@pytest.mark.django_db
class TestRetrieveManufacturer:
    """Test the /core/manufacturers/{manufacturer_id}/ API endpoint retrieving functionality."""

    def test_if_anonymous_user_retrieve_returns_401(self, create_manufacturer_instance, retrieve_manufacturer):
        """Test if anonymous user retrieve returns a 401 status"""
        manufacturer = create_manufacturer_instance()

        response = retrieve_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot retrieve a manufacturer'

    def test_if_authenticated_user_retrieve_returns_403(self, create_manufacturer_instance,
                                                        authenticate, retrieve_manufacturer):
        """Test if authenticated user retrieve returns a 403 status"""
        authenticate()
        manufacturer = create_manufacturer_instance()

        response = retrieve_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot retrieve a manufacturer'

    def test_if_staff_user_retrieve_returns_200(self, create_manufacturer_instance,
                                                authenticate, retrieve_manufacturer):
        """Test if staff user retrieve returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        manufacturer = create_manufacturer_instance()

        response = retrieve_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user can retrieve a specific manufacturer'
        assert {'id': response.data['id'], 'name': response.data['name']} == \
            {'id': manufacturer.id, 'name': manufacturer.name}, \
            'Assert that both database and response information about a manufacturer are equal'

    def test_if_staff_user_invalid_retrieve_returns_404(self,
                                                        authenticate, retrieve_manufacturer):
        """Test if staff user invalid retrieve returns a 404 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )

        response = retrieve_manufacturer(manufacturer_id=1)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            'Assert that a staff user cannot retrieve an invalid manufacturer'

    def test_if_superuser_retrieve_returns_200(self, create_manufacturer_instance,
                                               authenticate, retrieve_manufacturer):
        """Test if superuser retrieve returns a 200 status"""
        authenticate(is_superuser=True)
        manufacturer = create_manufacturer_instance()

        response = retrieve_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can retrieve a specific manufacturer'
        assert {'id': response.data['id'], 'name': response.data['name']} == \
            {'id': manufacturer.id, 'name': manufacturer.name}, \
            'Assert that both database and response information about a manufacturer are equal'

    def test_if_superuser_invalid_retrieve_returns_404(self,
                                                       authenticate, retrieve_manufacturer):
        """Test if superuser invalid retrieve returns a 404 status"""
        authenticate(is_superuser=True)

        response = retrieve_manufacturer(manufacturer_id=1)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            'Assert that a superuser cannot retrieve an invalid manufacturer'


@pytest.mark.django_db
class TestUpdateManufacturer:
    """Test the /core/manufacturers/{manufacturer_id} API endpoint updating functionality."""

    def test_if_anonymous_user_update_returns_401(self, create_manufacturer_instance, update_manufacturer):
        """Test if anonymous user update returns a 401 status"""
        manufacturer = create_manufacturer_instance()
        data = {'name': 'F Corp'}

        response = update_manufacturer(
            manufacturer_id=manufacturer.id, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot update a manufacturer'

    def test_if_authenticated_user_update_returns_403(self, create_manufacturer_instance,
                                                      authenticate, update_manufacturer):
        """Test if authenticated user update returns a 403 status"""
        authenticate()
        manufacturer = create_manufacturer_instance()
        data = {'name': 'F Corp'}

        response = update_manufacturer(
            manufacturer_id=manufacturer.id, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot update a manufacturer'

    def test_if_staff_user_update_returns_403(self, create_manufacturer_instance,
                                              authenticate, update_manufacturer):
        """Test if staff user update returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        manufacturer = create_manufacturer_instance()
        data = {'name': 'F Corp'}

        response = update_manufacturer(
            manufacturer_id=manufacturer.id, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot update a manufacturer'

    def test_if_superuser_update_returns_200(self, create_manufacturer_instance,
                                             authenticate, update_manufacturer):
        """Test if superuser update returns a 200 status"""
        authenticate(is_superuser=True)
        manufacturer = create_manufacturer_instance()
        data = {'name': 'F Corp'}

        response = update_manufacturer(
            manufacturer_id=manufacturer.id, data=data)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can update a specific manufacturer'
        assert response.data['name'] == data['name'], 'Assert that the name was updated.'


@pytest.mark.django_db
class TestDeleteManufacturer:
    """Test the /core/manufacturers/{manufacturer_id} API endpoint deleting functionality."""

    def test_if_anonymous_user_delete_returns_401(self, create_manufacturer_instance, delete_manufacturer):
        """Test if anonymous user delete returns a 401 status"""
        manufacturer = create_manufacturer_instance()

        response = delete_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot delete a manufacturer'

    def test_if_authenticated_user_delete_returns_403(self, create_manufacturer_instance,
                                                      authenticate, delete_manufacturer):
        """Test if authenticated user delete returns a 403 status"""
        authenticate()
        manufacturer = create_manufacturer_instance()

        response = delete_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot delete a manufacturer'

    def test_if_staff_user_delete_returns_403(self, create_manufacturer_instance,
                                              authenticate, delete_manufacturer):
        """Test if staff user delete returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        manufacturer = create_manufacturer_instance()

        response = delete_manufacturer(manufacturer_id=manufacturer.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot delete a manufacturer'

    def test_if_superuser_delete_returns_204(self, create_manufacturer_instance,
                                             authenticate, delete_manufacturer):
        """Test if superuser delete returns a 204 status"""
        authenticate(is_superuser=True)
        manufacturer = create_manufacturer_instance()

        response = delete_manufacturer(manufacturer_id=manufacturer.id)
        print(response.data)

        assert response.status_code == status.HTTP_204_NO_CONTENT, \
            'Assert that a superuser can delete a specific manufacturer'
