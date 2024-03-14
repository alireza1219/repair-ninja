from django.contrib.auth import get_user_model
from rest_framework import serializers
from repair_core.models import Category, Customer, Manufacturer, RepairMan, ServiceRequest, ServiceRequestItem


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
    user = UserProfileSerializer()

    class Meta:
        model = RepairMan
        fields = ['id', 'user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']


class ListServiceRequestSerializer(serializers.ModelSerializer):
    customer = SimpleCustomerSerializer()

    class Meta:
        model = ServiceRequest
        fields = ['id', 'placed_at', 'service_status',
                  'customer', 'service_priority']


class RetrieveServiceRequestSerializer(serializers.ModelSerializer):
    assigned_to = RepairManSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = ServiceRequest
        fields = '__all__'


class AddServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['service_status', 'service_priority', 'description',
                  'estimation_delivery', 'customer', 'assigned_to']


class UpdateServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['service_status', 'service_priority',
                  'description', 'estimation_delivery', 'assigned_to']


class ServiceRequestItemSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    category = CategorySerializer()

    class Meta:
        model = ServiceRequestItem
        fields = ['id', 'name', 'serial_number', 'condition',
                  'quantity', 'notes', 'manufacturer', 'category']


class AddServiceRequestItemSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        service_id = self.context['service_id']
        self.instance = ServiceRequestItem.objects.create(
            service_request_id=service_id, **self.validated_data)
        return self.instance

    class Meta:
        model = ServiceRequestItem
        fields = ['name', 'serial_number', 'condition',
                  'quantity', 'notes', 'manufacturer', 'category']


class UpdateServiceRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestItem
        fields = ['quantity', 'notes']
