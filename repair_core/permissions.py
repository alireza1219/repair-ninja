from rest_framework.permissions import BasePermission, IsAuthenticated, DjangoModelPermissions

REPAIRMAN_DEFAULT_PERMISSIONS = [
    # Customer model:
    'add_customer',
    'view_customer',
    # RepairMan model:
    'view_repairman',
    # Category model:
    'add_category',
    'view_category',
    # Manufacturer model:
    'add_manufacturer',
    'view_manufacturer',
    # Service model:
    'add_service',
    'change_service',
    'delete_service',
    'view_service',
    # ServiceItem model:
    'add_serviceitem',
    'change_serviceitem',
    'delete_serviceitem',
    'view_serviceitem',
]


class IsSuperUser(BasePermission):
    """Grant access to superusers."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CurrentUserOrSuperUser(IsAuthenticated):
    """Grant access to superusers or currently authenticated user."""

    def has_object_permission(self, request, view, obj):
        # Here's a resource for you:
        # https://stackoverflow.com/questions/43064417/whats-the-differences-between-has-object-permission-and-has-permission
        user = request.user
        return user.is_superuser or obj.pk == user.pk


class DjangoModelFullPermissions(DjangoModelPermissions):
    """
    Unfortunately, the core implementation of the base class was changed in
    DRF version 3.15.1
    https://github.com/encode/django-rest-framework/commit/4f10c4e43ee57f4a2e387e0c8d44d28d21a3621c
    This inherited implementation will bring back the GET HTTP request limitations.
    So, only the users with the right permissions can make a GET HTTP request.
    """

    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = ['%(app_label)s.view_%(model_name)s']
