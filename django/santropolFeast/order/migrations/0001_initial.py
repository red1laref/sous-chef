# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meal', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(verbose_name='date')),
                ('type', models.CharField(choices=[('ordered', 1), ('delivered', 2), ('no_charge', 3), ('paid', 4)], max_length=100, verbose_name='order_status')),
                ('value', models.CharField(max_length=20, verbose_name='value')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Client', verbose_name='client')),
            ],
            options={
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meal.Meal', verbose_name='meal')),
            ],
            options={
                'verbose_name_plural': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(related_name='order_items', to='order.OrderItem'),
        ),
    ]