from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import api_exceptions, models, serializers


class CustomerViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    queryset = models.Customer.objects.select_related('user') \
        .order_by('pk') \
        .all()
    serializer_class = serializers.CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        # Check if there's an association between a service and this customer object.
        if models.Service.objects.filter(customer_id=kwargs['pk']).count() > 0:
            return Response(
                {
                    'error': 'This customer is associated with one or more services and it cannot be deleted.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return super().destroy(request, *args, **kwargs)


class RepairManViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        GenericViewSet):
    queryset = models.RepairMan.objects.select_related('user') \
        .order_by('pk') \
        .all()
    serializer_class = serializers.RepairManSerializer


class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ManufacturerViewSet(ModelViewSet):
    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer


class ServiceViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
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
    http_method_names = ['get', 'post', 'patch', 'delete']

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
