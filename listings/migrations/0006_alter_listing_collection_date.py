# Generated by Django 4.1.2 on 2022-11-04 14:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_listing_collection_date_listing_timeslot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='collection_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
