from typing import Any
from urllib.parse import urlencode
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from . import models
from .utils import priority as get_priority


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']

    list_display = ['id', 'user_profile', 'first_name', 'last_name',
                    'email', 'phone', 'services']

    list_per_page = 10

    list_select_related = ['user']

    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    @admin.display(ordering='user__username', description='user profile')
    def user_profile(self, customer: models.Customer):
        user_admin_url = reverse(
            'admin:auth_user_change',
            args=[customer.user.id]
        )

        return format_html('<a href="{}">{}</a>', user_admin_url, customer.user.username)

    @admin.display(ordering='services')
    def services(self, customer: models.Customer):
        service_page_url = reverse(
            'admin:repair_core_service_changelist')

        url = (
            service_page_url
            + '?'
            + urlencode({
                'customer__id': str(customer.pk),
            })
        )

        count = customer.service_count

        return format_html('<a href="{}">{} Service(s)</a>', url, count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            service_count=Count('services')
        )


@admin.register(models.RepairMan)
class RepairManAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']

    list_display = ['id', 'user_profile', 'first_name', 'last_name',
                    'email', 'phone', 'service_assignments']

    list_per_page = 10

    list_select_related = ['user']

    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    @admin.display(ordering='user__username')
    def user_profile(self, repairman: models.RepairMan):
        user_admin_url = reverse(
            'admin:auth_user_change',
            args=[repairman.user.id]
        )

        return format_html('<a href="{}">{}</a>', user_admin_url, repairman.user.username)

    @admin.display(ordering='assignment_count')
    def service_assignments(self, repair_man: models.RepairMan):
        service_page_url = reverse(
            'admin:repair_core_service_changelist')

        url = (
            service_page_url
            + '?'
            + urlencode({
                'assigned_to': str(repair_man.pk),
            })
        )

        count = repair_man.assignment_count

        return format_html('<a href="{}">{} Assignment(s)</a>', url, count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            assignment_count=Count('assignments')
        )


@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 20
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 20
    search_fields = ['title']


class ServiceItemInline(admin.StackedInline):
    model = models.ServiceItem
    max_num = 10
    min_num = 1
    extra = 0
    autocomplete_fields = ['manufacturer', 'category']


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer', 'assigned_to']

    inlines = [ServiceItemInline]

    list_display = ['id', 'customer', 'placed_at',
                    'service_status', 'service_priority']

    list_per_page = 20

    ordering = ['-placed_at']

    # Here's an interesting finding for later read:
    # https://github.com/django/django/commit/85207a245b
    # https://stackoverflow.com/questions/6441084/django-filtering-by-filter-not-allowed

    @admin.display(ordering='priority')
    def service_priority(self, service: models.Service):
        return get_priority(service.priority)
