# Generated by Django 5.0.3 on 2024-03-17 19:24

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='RepairMan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_status', models.CharField(choices=[('R', 'Received'), ('I', 'In Progress'), ('C', 'Completed'), ('D', 'Delivered')], default='R', max_length=1)),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('priority', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0, message='Priority cannot be negative'), django.core.validators.MaxValueValidator(10, message='Priority cannot be higher than 10')])),
                ('description', models.TextField(blank=True, null=True)),
                ('estimation_delivery', models.DateField()),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='assignments', to='repair_core.repairman')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='repair_core.customer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='repair_core.category')),
                ('manufacturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='repair_core.manufacturer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='repair_core.service')),
            ],
        ),
    ]
