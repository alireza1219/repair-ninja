from rest_framework import serializers
from repair_core.models import Category, Customer, Manufacturer, RepairMan


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'email']


class RepairManSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairMan
        fields = ['id', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name']
