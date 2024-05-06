from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'type', 'permissions']
    
    def get_type(self, obj):
        if (obj.is_superuser):
            return "superuser"
        elif (obj.is_staff):
            return "staff"
        return "regular"

    def get_permissions(self, obj):
        User = get_user_model()
        all_permissions = User(is_superuser=True).get_all_permissions()
        # We're only interested in repair_core app permissions.
        repair_core_permissions = filter(
            lambda x: x.startswith('repair_core'), all_permissions)
        user_permissions = obj.get_all_permissions()
        return {p: p in user_permissions for p in repair_core_permissions}
