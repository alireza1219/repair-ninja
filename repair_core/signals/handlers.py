from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from repair_core.models import RepairMan


User = get_user_model()


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


@receiver(post_save, sender=RepairMan)
def add_repairman_default_permissions(sender, instance, created, **kwargs):
    """Assign a set of default permissions to a RepairMan object on its creation"""
    if created:
        try:
            repairman_user = User.objects.get(pk=instance.user_id)
        except User.DoesNotExist:
            # TODO: A simple logging might be nice here?
            return False

        permissions = Permission.objects.filter(
            codename__in=REPAIRMAN_DEFAULT_PERMISSIONS
        )

        # Assign the new permissions.
        repairman_user.user_permissions.set(permissions)

        # Mark the Repairman's user profile as a staff.
        User.objects.filter(pk=repairman_user.pk).update(is_staff=True)


@receiver(post_delete, sender=RepairMan)
def remove_repairman_permissions(sender, instance, **kwargs):
    """Remove permissions and revoke staff status when deleting a RepairMan object"""
    try:
        repairman_user = User.objects.get(pk=instance.user_id)
    except User.DoesNotExist:
        return False

    # Remove permissions assigned to the user
    repairman_user.user_permissions.clear()

    # Revoke staff status
    User.objects.filter(pk=repairman_user.pk).update(is_staff=False)
