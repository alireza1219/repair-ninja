from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import Category, Customer, Manufacturer, RepairMan, ServiceRequest, ServiceRequestItem
from . import serializers
from . import api_exceptions


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class RepairManViewSet(ReadOnlyModelViewSet):
    queryset = RepairMan.objects.select_related('user') \
        .order_by('pk') \
        .all()
    serializer_class = serializers.RepairManSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer


class ServiceRequestViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = ServiceRequest.objects.select_related('customer').all()

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('assigned_to__user')

        # FIXME: Extra queries when updating/creating a service request.

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RetrieveServiceRequestSerializer
        if self.request.method == 'POST':
            return serializers.AddServiceRequestSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateServiceRequestSerializer
        return serializers.ListServiceRequestSerializer


class ServiceRequestItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddServiceRequestItemSerializer
        if self.request.method == 'PATCH':
            return serializers.UpdateServiceRequestItemSerializer
        return serializers.ServiceRequestItemSerializer

    def get_serializer_context(self):
        return {'service_id': self.kwargs['service_pk']}

    def get_queryset(self):
        try:
            service_id = int(self.kwargs['service_pk'])
        except ValueError as e:
            raise api_exceptions.InvalidRequestException(str(e))

        # If the parent resource (here: ServiceRequest object) does not exists,
        # Instead of getting a 404 HTTP response, it'll return an empty list with a 200 HTTP response.
        # Turns out to be an issue with the drf nested routers:
        # https://github.com/alanjds/drf-nested-routers/issues/216
        # My workaround however, led to two extra sql queries. So I'm not going to use it for now!
        # service_object = get_object_or_404(ServiceRequest, pk=service_id)
        # queryset = service_object.items.all() \
        #     .select_related('manufacturer') \
        #     .select_related('category')

        queryset = ServiceRequestItem.objects \
            .filter(service_request_id=service_id) \
            .select_related('manufacturer') \
            .select_related('category')

        return queryset
