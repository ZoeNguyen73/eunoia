# Generated by Django 4.1.2 on 2022-10-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_groups_user_user_permissions_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]