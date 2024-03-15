from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']


class RepairMan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__list_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'  # It's not Categorys :lol:


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']


class Service(models.Model):
    SERVICE_RECEIVED = 'R'
    SERVICE_IN_PROGRESS = 'I'
    SERVICE_COMPLETED = 'C'
    SERVICE_DELIVERED = 'D'

    SERVICE_STATUS_CHOICES = [
        (SERVICE_RECEIVED, 'Received'),
        (SERVICE_IN_PROGRESS, 'In Progress'),
        (SERVICE_COMPLETED, 'Completed'),
        (SERVICE_DELIVERED, 'Delivered'),
    ]

    service_status = models.CharField(
        max_length=1, choices=SERVICE_STATUS_CHOICES, default=SERVICE_RECEIVED)
    placed_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(
        validators=[
            # 0 indicates high priority.
            MinValueValidator(0, message='Priority cannot be negative'),
            # 10 indicates low priority.
            MaxValueValidator(10, message='Priority cannot be higher than 10'),
        ],
        default=5
    )
    description = models.TextField(null=True, blank=True)
    estimation_delivery = models.DateField()
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT, related_name='services')
    assigned_to = models.ManyToManyField(
        to=RepairMan, related_name='assignments', blank=True)

    def __str__(self):
        return f"Service ID #{self.pk}"

    class Meta:
        ordering = ['id']


class ServiceItem(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    quantity = models.IntegerField(
        default=1, validators=[MinValueValidator(0)])
    notes = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(
        to=Manufacturer, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(
        to=Category, on_delete=models.PROTECT, null=True)
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name='items')

    def __str__(self):
        if self.manufacturer:
            return f"{self.name} Manufactured by {self.manufacturer} in {self.service}"
        return f"{self.name} in {self.service}"
