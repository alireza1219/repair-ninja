from django.test import TestCase
from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.test import APIClient


from repair_core.models import RepairMan
from repair_core.signals import handlers


class RepairManTestCase(TestCase):
    """
    RepairMan model testcases.
    """

    def setUp(self):
        # Prepare the API endpoints path that will be tested.
        self.auth_endpoint = '/auth/jwt/create/'
        self.category_endpoint = '/core/categories/'
        self.customer_endpoint = '/core/customers/'
        self.manufacturer_endpoint = '/core/manufacturers/'
        self.repairman_endpoint = '/core/repairmen/'
        self.service_endpoint = '/core/services/'
        self.user_endpoint = '/auth/users/'

        # Store the authentication constants for later use.
        self.auth_username = 'awesome_repairman'
        self.auth_password = 'awesome_password'
        self.auth_email = 'awesome@repairman.local'
        self.auth_first_name = 'Repair'
        self.auth_last_name = 'Man'

        # Create a User instance and store it inside the self.user.
        self.user = User.objects.create_user(
            username=self.auth_username,
            password=self.auth_password,
            email=self.auth_email,
            first_name=self.auth_first_name,
            last_name=self.auth_last_name
        )

    def test_repairman_permissions(self):
        """
        Check if an associated User to a RepairMan has the right permissions after creation and deletion.
        """
        # Create a RepairMan instance.
        repairman = RepairMan.objects.create(
            user=self.user,
            phone='123456789'
        )

        queryset = User.objects.filter(pk=self.user.id)
        updated_user = queryset.get()

        # Check if the User instance has been marked as a staff.
        self.assertTrue(
            updated_user.is_staff,
            'Assert that the user is a staff member'
        )

        # Check if the User instance has the right permissions as a RepairMan.
        perm_queryset = Permission.objects.filter(
            codename__in=handlers.REPAIRMAN_DEFAULT_PERMISSIONS
        )
        permissions = [
            f"{perm.content_type.app_label}.{perm.codename}" for perm in perm_queryset
        ]
        # Here's a resource for you:
        # https://docs.djangoproject.com/en/5.0/ref/contrib/auth/#django.contrib.auth.models.User.has_perms
        self.assertTrue(
            updated_user.has_perms(permissions),
            'Assert that the user has the necessary permissions for the RepairMan role.'
        )

        # Delete the RepairMan instance.
        repairman.delete()
        updated_user = queryset.get()

        # Check if the associated User is no longer marked as staff.
        self.assertFalse(
            updated_user.is_staff,
            'Assert that the user is not a staff member.'
        )

        # Check if the associated User no longer has the permissions.
        self.assertFalse(
            updated_user.has_perms(permissions),
            'Assert that the user does not have the permissions required for the RepairMan role.'
        )

    def test_repairman_api_access_level(self):
        """
        Test the access level of a RepairMan User across various API endpoints.
        """
        # Create a RepairMan instance, again.
        repairman = RepairMan.objects.create(
            user=self.user,
            phone='123456789'
        )

        # Try to authenticate with the given credentials first.
        data = {
            'username': self.auth_username,
            'password': self.auth_password
        }
        response = self.client.post(self.auth_endpoint, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            'Assert that the authentication succeeded.'
        )
        self.assertTrue(
            'refresh' and 'access' in response.data,
            'Assert that the response data contains both refresh and access key tokens.'
        )

        # Store the access key token for later use.
        auth_key = response.data['access']
        # Create a custom authorized client for later use.
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"JWT {auth_key}")

        # A RepairMan cannot create a new RepairMan instance using the API.
        data = {
            'user_id': 2,
            'phone': '1234'
        }
        response = client.post(self.repairman_endpoint, data, format='json')
        self.assertTrue(
            response.status_code == status.HTTP_403_FORBIDDEN,
            'Assert that a RepairMan cannot create a new RepairMan instance using the API endpoint.'
        )

        # A RepairMan cannot delete an existing RepairMan instance using the API.
        response = client.delete(f"{self.repairman_endpoint}{repairman.id}/")
        self.assertTrue(
            response.status_code == status.HTTP_403_FORBIDDEN,
            'Assert that a RepairMan cannot delete an existing RepairMan instance using the API endpoint.'
        )

        # Create a temp user then associate it with a customer.
        # So, it's possible to test if a RepairMan is able to create a customer.
        test_user = User.objects.create_user(
            username='customer_username',
            password='customer_password'
        )
        # First, check if the customers endpoint is accessible by the RepairMan.
        response = client.get(self.customer_endpoint)
        self.assertTrue(
            response.status_code == status.HTTP_200_OK,
            'Assert that a RepairMan has access to customer API endpoint.'
        )
        # Now, try to create a new customer.
        data = {
            'user_id': test_user.id,
            'phone': '1234567890'
        }
        response = client.post(self.customer_endpoint, data, format='json')
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED,
            'Assert that a RepairMan can create a new Customer instance using the API endpoint.'
        )

        # Try to create a new Category using the API endpoint.
        data = {
            'title': 'Laptop'
        }
        response = client.post(self.category_endpoint, data, format='json')
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED and 'id' in response.data,
            'Assert that a RepairMan can create a new Category instance using the API endpoint.'
        )

        # Grab the newly created category id for later use.
        new_category_id = response.data['id']

        # Try to create a new Manufacturer using the API endpoint.
        data = {
            'name': 'E Corp'
        }
        response = client.post(self.manufacturer_endpoint, data, format='json')
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED and 'id' in response.data,
            'Assert that a RepairMan can create a new Manufacturer instance using the API endpoint.'
        )

        # Grab the newly created manufacturer id for later use.
        new_manufacturer_id = response.data['id']

        # Try to create a new User instance using the API endpoint.
        data = {
            'username': 'lorem',
            'password': 'ipsum',
            'email': 'awesome@user.local',
            'first_name': '12',
            'last_name': '19'
        }
        response = client.post(self.user_endpoint, data, format='json')

        # Grab the newly created user id for later use.
        new_user_id = response.data['id']

        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED and 'id' in response.data,
            'Assert that a RepairMan can create a new User instance using the API endpoint.'
        )

        # Try to create a new service.
        # Before doing anything, associate the new user with a customer.
        data = {
            'user_id': new_user_id,
            'phone': '11112222'
        }
        response = client.post(self.customer_endpoint, data, format='json')

        # Grab the newly created customer id for later use.
        new_customer_id = response.data['id']

        data = {
            'estimation_delivery': '2038-01-19',
            'customer': new_customer_id,
        }
        response = client.post(self.service_endpoint, data, formst='json')
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED and 'id' in response.data,
            'Assert that a RepairMan can create a new User instance using the API endpoint.'
        )

        # Grab the newly created service id for later use.
        new_service_id = response.data['id']

        # Now try to add some items to this service.
        data = {
            'name': 'E Laptop Pro',
            'serial_number': '913e21',
            'condition': 'No Power',
            'notes': 'The board was water damaged.',
            'manufacturer': new_manufacturer_id,
            'category': new_category_id
        }
        response = client.post(
            f"{self.service_endpoint}{new_service_id}/items/",
            data,
            format='json'
        )
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED,
            'Assert that a RepairMan can add a Service Item using the API endpoint.'
        )

        # Check the remaining API accesses.
        response = client.get(self.service_endpoint)
        self.assertTrue(
            response.status_code == status.HTTP_200_OK,
            'Assert that a RepairMan has access to service API endpoint.'
        )

        response = client.get(self.category_endpoint)
        self.assertTrue(
            response.status_code == status.HTTP_200_OK,
            'Assert that a RepairMan has access to category API endpoint.'
        )

        response = client.get(self.manufacturer_endpoint)
        self.assertTrue(
            response.status_code == status.HTTP_200_OK,
            'Assert that a RepairMan has access to manufacturer API endpoint.'
        )

        # Revoke the RepairMan access level.
        repairman.delete()
        # Cannot list categories.
        response = client.get(self.category_endpoint)
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)
        # Cannot retrieve a Service instance.
        response = client.get(f"{self.service_endpoint}{new_service_id}/")
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND)
        # Cannot perform POST request.
        response = client.post(self.service_endpoint)
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)
        # Cannot list manufacturers.
        response = client.get(self.manufacturer_endpoint)
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)
