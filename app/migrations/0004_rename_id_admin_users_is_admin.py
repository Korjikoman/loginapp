# Generated by Django 4.2.15 on 2025-02-16 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_is_staff_users_id_admin_users_is_verified_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='id_admin',
            new_name='is_admin',
        ),
    ]
