import pytest

from rest_framework import status

from repair_core.models import Category
from repair_core.permissions import REPAIRMAN_DEFAULT_PERMISSIONS


@pytest.fixture(name='create_category_instance')
def fixture_create_category_instance():
    """Create and return a Category instance."""
    def _create_category_instance(title='Laptop'):
        return Category.objects.create(title=title)
    return _create_category_instance


@pytest.fixture(name='get_categories_list')
def fixture_get_categories_list(api_client):
    """Perform HTTP GET request on /core/categories/ API endpoint."""
    def _get_categories_list():
        return api_client.get('/core/categories/')
    return _get_categories_list


@pytest.fixture(name='create_category')
def fixture_create_category(api_client):
    """Perform HTTP POST request on /core/categories/ API endpoint."""
    def _create_category(data: dict):
        return api_client.post('/core/categories/', data, format='json')
    return _create_category


@pytest.fixture(name='retrieve_category')
def fixture_retrieve_category(api_client):
    """Retrieve a specific category using /core/categories/{category_id}/ endpoint."""
    def _retrieve_category(category_id: int):
        return api_client.get(f"/core/categories/{category_id}/")
    return _retrieve_category


@pytest.fixture(name='update_category')
def fixture_update_category(api_client):
    """Perform HTTP PATCH request on /core/categories/{category_id}/ endpoint."""
    def _update_category(category_id: int, data: dict):
        return api_client.patch(f"/core/categories/{category_id}/", data, format='json')
    return _update_category


@pytest.fixture(name='delete_category')
def fixture_delete_category(api_client):
    """Perform HTTP DELETE request on /core/categories/{category_id}/ endpoint."""
    def _delete_category(category_id: int):
        return api_client.delete(f"/core/categories/{category_id}/")
    return _delete_category


@pytest.mark.django_db
class TestListCategories:
    """Test the /core/categories/ API endpoint listing functionality."""

    def test_if_anonymous_user_get_request_returns_401(self, get_categories_list):
        """Test if anonymous user GET HTTP request returns a 401 status"""
        response = get_categories_list()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot list the categories'

    def test_if_authenticated_user_get_request_returns_403(self, authenticate, get_categories_list):
        """Test if authenticated user GET HTTP request returns a 403 status"""
        authenticate()

        response = get_categories_list()

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot list the categories'

    def test_if_staff_user_get_request_returns_200(self, authenticate, get_categories_list):
        """Test if staff user GET HTTP request returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )

        response = get_categories_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user can list the categories'

    def test_if_superuser_get_request_returns_200(self, authenticate, get_categories_list):
        """Test if superuser GET HTTP request returns a 200 status"""
        authenticate(is_superuser=True)

        response = get_categories_list()

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can list the categories'


@pytest.mark.django_db
class TestCreateCategory:
    """Test creating a new category using the /core/categories/ API endpoint."""

    def test_if_anonymous_user_create_returns_401(self, create_category):
        """Test if anonymous user create returns a 401 status"""
        data = {'title': 'Laptop'}

        response = create_category(data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot create a new category'

    def test_if_authenticated_user_create_returns_403(self, authenticate, create_category):
        """Test if authenticated user create returns a 403 status"""
        authenticate()
        data = {'title': 'Laptop'}

        response = create_category(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot create a new category'

    def test_if_staff_user_create_returns_201(self, authenticate, create_category):
        """Test if staff user create returns a 201 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        data = {'title': 'Laptop'}

        response = create_category(data)

        assert response.status_code == status.HTTP_201_CREATED, \
            'Assert that an authenticated staff user cannot create a new category'
        assert response.data['id'] > 0, 'Assert that the category id is present in response body'
        assert response.data['title'] == data['title'], 'Assert the equality of titles'

    def test_if_staff_user_create_using_invalid_data_returns_400(self,
                                                                 authenticate, create_category):
        """Test if staff user create using invalid data returns a 400 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        data = {}

        response = create_category(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            'Assert that a staff user cannot create a new category using invalid data'

    def test_if_superuser_create_returns_201(self, authenticate, create_category):
        """Test if superuser create returns a 201 status"""
        authenticate(is_superuser=True)
        data = {'title': 'Laptop'}

        response = create_category(data)

        assert response.status_code == status.HTTP_201_CREATED, \
            'Assert that a superuser can create a new category using the API'
        assert response.data['id'] > 0, 'Assert that the category id is present in response body'
        assert response.data['title'] == data['title'], 'Assert the equality of titles'

    def test_if_superuser_create_using_invalid_data_returns_400(self,
                                                                authenticate, create_category):
        """Test if superuser create using invalid data returns a 400 status"""
        authenticate(is_superuser=True)
        data = {}

        response = create_category(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, \
            'Assert that a staff user cannot create a new category using invalid data'


@pytest.mark.django_db
class TestRetrieveCategory:
    """Test the /core/categories/{category_id}/ API endpoint retrieving functionality."""

    def test_if_anonymous_user_retrieve_returns_401(self, create_category_instance, retrieve_category):
        """Test if anonymous user retrieve returns a 401 status"""
        category = create_category_instance()

        response = retrieve_category(category_id=category.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot retrieve a category'

    def test_if_authenticated_user_retrieve_returns_403(self, create_category_instance,
                                                        authenticate, retrieve_category):
        """Test if authenticated user retrieve returns a 403 status"""
        authenticate()
        category = create_category_instance()

        response = retrieve_category(category_id=category.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot retrieve a category'

    def test_if_staff_user_retrieve_returns_200(self, create_category_instance,
                                                authenticate, retrieve_category):
        """Test if staff user retrieve returns a 200 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        category = create_category_instance()

        response = retrieve_category(category_id=category.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that an authenticated staff user can retrieve a specific category'
        assert {'id': response.data['id'], 'title': response.data['title']} == \
            {'id': category.id, 'title': category.title}, \
            'Assert that both database and response information about a category are equal'

    def test_if_staff_user_invalid_retrieve_returns_404(self,
                                                        authenticate, retrieve_category):
        """Test if staff user invalid retrieve returns a 404 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )

        response = retrieve_category(category_id=1)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            'Assert that a staff user cannot retrieve an invalid category'

    def test_if_superuser_retrieve_returns_200(self, create_category_instance,
                                               authenticate, retrieve_category):
        """Test if superuser retrieve returns a 200 status"""
        authenticate(is_superuser=True)
        category = create_category_instance()

        response = retrieve_category(category_id=category.id)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can retrieve a specific category'
        assert {'id': response.data['id'], 'title': response.data['title']} == \
            {'id': category.id, 'title': category.title}, \
            'Assert that both database and response information about a category are equal'

    def test_if_superuser_invalid_retrieve_returns_404(self,
                                                       authenticate, retrieve_category):
        """Test if superuser invalid retrieve returns a 404 status"""
        authenticate(is_superuser=True)

        response = retrieve_category(category_id=1)

        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            'Assert that a superuser cannot retrieve an invalid category'


@pytest.mark.django_db
class TestUpdateCategory:
    """Test the /core/categories/{category_id} API endpoint updating functionality."""

    def test_if_anonymous_user_update_returns_401(self, create_category_instance, update_category):
        """Test if anonymous user update returns a 401 status"""
        category = create_category_instance()
        data = {'title': 'Mobile Phone'}

        response = update_category(category_id=category.id, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot update a category'

    def test_if_authenticated_user_update_returns_403(self, create_category_instance,
                                                      authenticate, update_category):
        """Test if authenticated user update returns a 403 status"""
        authenticate()
        category = create_category_instance()
        data = {'title': 'Mobile Phone'}

        response = update_category(category_id=category.id, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot update a category'

    def test_if_staff_user_update_returns_403(self, create_category_instance,
                                              authenticate, update_category):
        """Test if staff user update returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        category = create_category_instance()
        data = {'title': 'Mobile Phone'}

        response = update_category(category_id=category.id, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot update a category'

    def test_if_superuser_update_returns_200(self, create_category_instance,
                                             authenticate, update_category):
        """Test if superuser update returns a 200 status"""
        authenticate(is_superuser=True)
        category = create_category_instance()
        data = {'title': 'Mobile Phone'}

        response = update_category(category_id=category.id, data=data)

        assert response.status_code == status.HTTP_200_OK, \
            'Assert that a superuser can update a specific category'
        assert response.data['title'] == data['title'], 'Assert that the title was updated.'


@pytest.mark.django_db
class TestDeleteCategory:
    """Test the /core/categories/{category_id} API endpoint deleting functionality."""

    def test_if_anonymous_user_delete_returns_401(self, create_category_instance, delete_category):
        """Test if anonymous user delete returns a 401 status"""
        category = create_category_instance()

        response = delete_category(category_id=category.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            'Assert that an anonymous user cannot delete a category'

    def test_if_authenticated_user_delete_returns_403(self, create_category_instance,
                                                      authenticate, delete_category):
        """Test if authenticated user delete returns a 403 status"""
        authenticate()
        category = create_category_instance()

        response = delete_category(category_id=category.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated user cannot delete a category'

    def test_if_staff_user_delete_returns_403(self, create_category_instance,
                                              authenticate, delete_category):
        """Test if staff user delete returns a 403 status"""
        authenticate(
            is_staff=True,
            permissions=REPAIRMAN_DEFAULT_PERMISSIONS
        )
        category = create_category_instance()

        response = delete_category(category_id=category.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            'Assert that an authenticated staff user cannot delete a category'

    def test_if_superuser_delete_returns_204(self, create_category_instance,
                                             authenticate, delete_category):
        """Test if superuser delete returns a 204 status"""
        authenticate(is_superuser=True)
        category = create_category_instance()

        response = delete_category(category_id=category.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT, \
            'Assert that a superuser can delete a specific category'
