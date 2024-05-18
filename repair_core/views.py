from django.db.models import Count
from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

from . import api_exceptions, models, serializers, pagination
from .permissions import DjangoModelFullPermissions


class ServiceStatisticsViewSet(ViewSet):
    """
    Providing an overview of service metrics for the client dashboard.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: HttpRequest, format=None) -> Response:
        """
        Process the get request.
        """
        queryset = models.Service.objects.none()

        if request.user.is_staff:
            # Get all service objects.
            queryset = models.Service.objects.all() \
                .only('service_status')
        else:
            user_id = request.user.id
            try:
                customer_id = models.Customer.objects \
                    .only('id').get(user_id=user_id)
            except models.Customer.DoesNotExist:
                return Response(
                    data={
                        'errors': [
                            {
                                'code': '404_not_found',
                                'detail': 'There is no customer associated with this user ID.',
                            }
                        ]
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            # Filter all the service objects that belongs the this customer.
            queryset = models.Service.objects.filter(customer_id=customer_id) \
                .only('service_status')

        count_queryset = queryset.values('service_status')\
            .annotate(status_count=Count('service_status'))
        data = {entry['service_status']: entry['status_count']
                for entry in count_queryset}
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


class CustomerViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        GenericViewSet):
    """
    An API endpoint for managing customers.
    """
    filter_backends = [SearchFilter]
    pagination_class = pagination.DefaultPagination
    permission_classes = [DjangoModelFullPermissions]
    queryset = models.Customer.objects.select_related('user') \
        .order_by('pk') \
        .all()
    serializer_class = serializers.CustomerSerializer
    search_fields = ['user__first_name',
                     'user__last_name', 'user__username', 'user__email', 'phone']


class RepairManViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        GenericViewSet):
    """
    An API endpoint for managing repairmen.
    """
    filter_backends = [SearchFilter]
    pagination_class = pagination.DefaultPagination
    permission_classes = [DjangoModelFullPermissions]
    queryset = models.RepairMan.objects.select_related('user') \
        .order_by('pk') \
        .all()
    serializer_class = serializers.RepairManSerializer
    search_fields = ['user__first_name',
                     'user__last_name', 'user__username', 'user__email', 'phone']


class CategoryViewSet(ModelViewSet):
    """
    An API endpoint for managing categories.
    """
    filter_backends = [SearchFilter]
    pagination_class = pagination.DefaultPagination
    permission_classes = [DjangoModelFullPermissions]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    search_fields = ['title']


class ManufacturerViewSet(ModelViewSet):
    """
    An API endpoint for managing manufacturers.
    """
    filter_backends = [SearchFilter]
    pagination_class = pagination.DefaultPagination
    permission_classes = [DjangoModelFullPermissions]
    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer
    search_fields = ['name']


class ServiceViewSet(ModelViewSet):
    """
    An API endpoint for managing services.
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # TODO: Priority less than, greater than filtering.
    # The front-end is not capable of this at the moment. So, I'm going to ignore it for now.
    filterset_fields = ['customer_id', 'priority', 'service_status']
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    pagination_class = pagination.DefaultPagination
    ordering_fields = ['id', 'priority', 'last_update', 'placed_at']

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return [DjangoModelFullPermissions()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Only process the customer's services.
        if not self.request.user.is_staff:
            # The authenticated user's id.
            user_id = self.request.user.id

            try:
                # The customer profile associated with this user.
                customer_id = models.Customer.objects.only('id') \
                    .get(user_id=user_id)
            except models.Customer.DoesNotExist:
                # TODO: Logging, Maybe?
                return models.Service.objects.none()

            queryset = models.Service.objects.filter(customer_id=customer_id)
            return queryset

        queryset = models.Service.objects.select_related(
            'customer__user').all()

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('assigned_to__user')

        # About the extra queries when updating/creating a service:
        # It happens when assigning a service to multiple repairmen.
        # The DRF tries to validate all the given IDs where each validation is -
        # relevant to an extra select query on the RepairMan database table.
        # Once everything is validated, it'll execute another extra query to -
        # update service assignees.
        # The job gets done by calling the .set() method on a query set.

        return queryset

    def get_serializer_class(self):
        # A customer has its own service serializer.
        if not self.request.user.is_staff:
            return serializers.BasicServiceSerializer

        # The serializers below were defined for the staff members.
        if self.action == 'retrieve':
            return serializers.RetrieveServiceSerializer
        if self.request.method == 'POST':
            return serializers.CreateServiceSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateServiceSerializer
        return serializers.ListServiceSerializer

    def destroy(self, request, *args, **kwargs):
        if models.ServiceItem.objects.filter(service_id=kwargs['pk']).count() > 0:
            return Response(
                {
                    'error': 'This service is associated with one or more items and it cannot be deleted.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return super().destroy(request, *args, **kwargs)


class ServiceItemViewSet(ModelViewSet):
    """
    An API endpoint for managing service items.
    """
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    # TODO: Customer access.
    pagination_class = pagination.DefaultPagination
    permission_classes = [DjangoModelFullPermissions]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddServiceItemSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateServiceItemSerializer
        return serializers.ServiceItemSerializer

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}

    def get_queryset(self):
        try:
            service_id = int(self.kwargs['service_pk'])
        except ValueError as e:
            raise api_exceptions.InvalidRequestException(str(e))

        # If the parent resource (here: Service object) does not exists,
        # Instead of getting a 404 HTTP response, it'll return an empty list with a 200 HTTP response.
        # Turns out to be an issue with the drf nested routers:
        # https://github.com/alanjds/drf-nested-routers/issues/216
        # My workaround however, led to two extra sql queries. So I'm not going to use it for now!
        # service_object = get_object_or_404(Service, pk=service_id)
        # queryset = service_object.items.all() \
        #     .select_related('manufacturer') \
        #     .select_related('category')

        queryset = models.ServiceItem.objects \
            .filter(service_id=service_id) \
            .select_related('manufacturer') \
            .select_related('category')

        return queryset
