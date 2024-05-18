from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from repair_core.models import Customer, RepairMan, Service


class UserCreateSerializer(BaseUserCreateSerializer):
    email = serializers.EmailField(required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

    def validate_email(self, value):
        """
        Validate the email when creating a new user instance.
        """
        User = get_user_model()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with that email already exists.")
        return value


class UserSerializer(BaseUserSerializer):
    email = serializers.EmailField(required=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'type']

    def validate_email(self, value):
        """
        Validate the email when updating a user instance.
        """
        User = get_user_model()
        instance = self.instance
        error_message = "A user with that email already exists."
        if instance and instance.pk:
            if User.objects.filter(email=value).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError(error_message)
        # The user-create serializer is separate from this serializer.
        # And the alternative flow is not going to be executed.
        # But I'm keeping it for now, just in case things go wrong.
        else:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(error_message)
        return value

    def get_type(self, obj):
        if obj.is_superuser:
            return "superuser"
        if obj.is_staff:
            return "staff"
        return "regular"


class UserProfileSerializer(UserSerializer):
    """
    Djoser's /users/me/ Endpoint
    """
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['permissions']

    def get_permissions(self, obj):
        User = get_user_model()
        all_permissions = User(is_superuser=True).get_all_permissions()
        # We're only interested in repair_core app permissions.
        repair_core_permissions = filter(
            lambda x: x.startswith('repair_core'), all_permissions)
        user_permissions = obj.get_all_permissions()
        return {p: p in user_permissions for p in repair_core_permissions}


class UserDeleteSerializer(serializers.Serializer):
    """
    It wasn't possible to override Djoser's view classes in the settings.
    Instead, we can use this delete serializer to raise a validation error
    in cases where user is associated with one or more services.
    """
    confirm = serializers.CharField(required=True, max_length=255)

    def validate_confirm(self, value):
        """
        Confirm the deletion request by manually typing the instance's username
        """
        instance = self.instance
        if value != instance.username:
            raise serializers.ValidationError("Username does not match!")

        return value

    def validate(self, attrs):
        instance = self.instance
        error_message = {
            "integrity": "This User is associated with one or more services and it cannot be deleted."
        }
        # First check if this user is associated with a customer profile
        if Customer.objects.filter(user_id=instance.pk).exists():
            customer = Customer.objects.get(user_id=instance.pk)
            if Service.objects.filter(customer=customer).count() > 0:
                raise serializers.ValidationError(error_message)

        # Otherwise, check if this user is associated with a repairman profile
        # (A Little Note: Repairmen have a many-to-many relation with the service model,
        # and it's possible to delete them without an integrity check)
        elif RepairMan.objects.filter(user_id=instance.pk).exists():
            repairman = RepairMan.objects.get(user_id=instance.pk)
            if Service.objects.filter(assigned_to=repairman).count() > 0:
                raise serializers.ValidationError(error_message)

        return super().validate(attrs)
