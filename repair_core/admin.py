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
    list_display = ['first_name', 'last_name',
                    'email', 'phone', 'services']
    list_select_related = ['user']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']

    @admin.display(ordering='services')
    def services(self, customer: models.Customer):
        service_page_url = reverse(
            'admin:repair_core_service_changelist')

        url = (
            service_page_url
            + '?'
            + urlencode({
                'user_type': 'customer',
                'customer': str(customer.pk)
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
    list_display = ['first_name', 'last_name', 'service_assignments']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']

    @admin.display(ordering='assignment_count')
    def service_assignments(self, repair_man: models.RepairMan):
        service_page_url = reverse(
            'admin:repair_core_service_changelist')

        url = (
            service_page_url
            + '?'
            + urlencode({
                'user_type': 'repairman',
                'assigned_to': str(repair_man.pk)
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
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


class ServiceItemInline(admin.StackedInline):
    model = models.ServiceItem
    max_num = 10
    min_num = 1
    extra = 0
    autocomplete_fields = ['manufacturer', 'category']


class UserTypeFilter(admin.SimpleListFilter):
    title = 'User Type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return (
            ('customer', 'Customer'),
            ('repairman', 'Repair Man'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        user_id = request.GET.get('user_id')

        if value == 'customer':
            customers = models.Customer.objects.values_list('user', flat=True)
            if user_id:
                customers = customers.filter(user_id=user_id)
            return queryset.filter(customer__in=customers)
        if value == 'repairman':
            repairmen = models.RepairMan.objects.values_list('user', flat=True)
            if user_id:
                repairmen = repairmen.filter(user_id=user_id)
            return queryset.filter(assigned_to__in=repairmen)
        return queryset


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'service_status',
                    'customer', 'priority']
    autocomplete_fields = ['customer', 'assigned_to']
    list_filter = [UserTypeFilter, 'assigned_to', 'customer']  # FIXME Later...
    inlines = [ServiceItemInline]

    @admin.display(ordering='priority')
    def priority(self, service: models.Service):
        return get_priority(service.priority)
