from rest_framework.viewsets import ModelViewSet
from .models import Category, Customer, Manufacturer, RepairMan
from . import serializers


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class RepairManViewSet(ModelViewSet):
    queryset = RepairMan.objects.select_related('user').all()
    serializer_class = serializers.RepairManSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerSerializer
