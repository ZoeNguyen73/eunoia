# Generated by Django 4.1.2 on 2022-10-23 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_added_users_organizations_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
