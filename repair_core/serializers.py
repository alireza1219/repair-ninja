from django.contrib.auth import get_user_model
from rest_framework import serializers
from repair_core.models import Category, Customer, Manufacturer, RepairMan, Service, ServiceItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'email']


class SimpleCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class RepairManSerializer(serializers.ModelSerializer):
    details = UserProfileSerializer(source='user')

    class Meta:
        model = RepairMan
        fields = ['user_id', 'details']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']


class ListServiceSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer()

    class Meta:
        model = Service
        fields = ['id', 'placed_at', 'service_status',
                  'customer', 'priority']


class RetrieveServiceSerializer(serializers.ModelSerializer):
    assigned_to = RepairManSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Service
        fields = '__all__'


class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_status', 'priority', 'description',
                  'estimation_delivery', 'customer', 'assigned_to']


class UpdateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_status', 'priority',
                  'description', 'estimation_delivery', 'assigned_to']


class ServiceItemSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    category = CategorySerializer()

    class Meta:
        model = ServiceItem
        fields = ['id', 'name', 'serial_number', 'condition',
                  'quantity', 'notes', 'manufacturer', 'category']


class AddServiceItemSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        service_id = self.context['service_id']
        self.instance = ServiceItem.objects.create(
            service_id=service_id, **self.validated_data)
        return self.instance

    class Meta:
        model = ServiceItem
        fields = ['name', 'serial_number', 'condition',
                  'quantity', 'notes', 'manufacturer', 'category']


class UpdateServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = ['quantity', 'notes']
