from rest_framework.permissions import BasePermission, IsAuthenticated


# Here's some resources for you:
# https://stackoverflow.com/questions/43064417/whats-the-differences-between-has-object-permission-and-has-permission


class IsSuperUser(BasePermission):
    """Grant access to superusers."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CurrentUserOrSuperUser(IsAuthenticated):
    """Grant access to superusers or currently authenticated user."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_superuser or obj.pk == user.pk
