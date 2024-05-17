from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


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
