from django.contrib.auth import get_user_model
from rest_framework import serializers
from repair_core.models import Category, Customer, Manufacturer, RepairMan, Service, ServiceItem


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    user_profile = UserProfileSerializer(source='user', read_only=True)

    def validate_user_id(self, user_id: int):
        """
        Validate the posted user_id value.
        """
        # First, check for a User object with the given ID.
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError(
                'a user with this id does not exists.')

        # Second, check for a current customer with the given ID.
        if Customer.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                'customer with this user already exists.')

        # Then, double check for a RepairMan object with the given ID.
        if RepairMan.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                'a user cannot be both a customer and a repairman.')

        # Validation completed! Return the value.
        return user_id

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'user_profile', 'phone']


class RepairManSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    user_profile = UserProfileSerializer(source='user', read_only=True)

    def validate_user_id(self, user_id: int):
        """
        Validate the posted user_id value.
        """
        # First, check for a User object with the given ID.
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError(
                'a user with this id does not exists.')

        # Second, check for a current repairman with the given ID.
        if RepairMan.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                'repair man with this user already exists.')

        # Then, double check for a Customer object with the given ID.
        if Customer.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError(
                'a user cannot be both a customer and a repairman.')

        # Validation completed! Return the value.
        return user_id

    class Meta:
        model = RepairMan
        fields = ['id', 'user_id', 'user_profile', 'phone']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']


class BasicServiceSerializer(serializers.ModelSerializer):
    """
    This is a basic version of Service model serializer
    which is mainly used with the customers.
    """
    class Meta:
        model = Service
        fields = ['id', 'service_status', 'placed_at',
                  'last_update', 'description', 'estimation_delivery']


class ListServiceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

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
