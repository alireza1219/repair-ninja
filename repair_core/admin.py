from typing import Any
from urllib.parse import urlencode
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from repair_core import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'phone', 'service_requests']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='service_requests')
    def service_requests(self, customer: models.Customer):
        service_request_page_url = reverse(
            'admin:repair_core_servicerequest_changelist')

        url = (
            service_request_page_url
            + '?'
            + urlencode({
                'customer__id': str(customer.pk)
            })
        )

        count = customer.service_requests

        return format_html('<a href="{}">{} Service Request(s)</a>', url, count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            service_requests=Count('servicerequest')
        )


@admin.register(models.RepairMan)
class RepairManAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'service_assignees']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']

    @admin.display(ordering='assignee_count')
    def service_assignees(self, repair_man: models.RepairMan):
        service_request_page_url = reverse(
            'admin:repair_core_servicerequest_changelist')

        url = (
            service_request_page_url
            + '?'
            + urlencode({
                'assigned_to__id': str(repair_man.pk)
            })
        )

        count = repair_man.assignee_count

        return format_html('<a href="{}">{} Service Assignee(s)</a>', url, count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            assignee_count=Count('service_requests')
        )


@admin.register(models.Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


class ServiceRequestItemInline(admin.StackedInline):
    model = models.ServiceRequestItem
    max_num = 10
    min_num = 1
    extra = 0
    autocomplete_fields = ['manufacturer', 'category']


@admin.register(models.ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'service_status',
                    'customer', 'priority']
    autocomplete_fields = ['customer', 'assigned_to']
    inlines = [ServiceRequestItemInline]

    @admin.display(ordering='service_priority')
    def priority(self, service_request: models.ServiceRequest):
        PRIORITY_DICT = {
            0: 'Highest',
            1: 'Very High',
            2: 'High',
            3: 'Above Average',
            4: 'Average',
            5: 'Below Average',
            6: 'Low',
            7: 'Very Low',
            8: 'Lowest',
            9: 'Extremely Low',
            10: 'Not Specified'
        }
        return PRIORITY_DICT[service_request.service_priority]
