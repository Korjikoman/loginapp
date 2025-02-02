# Generated by Django 4.2.15 on 2025-02-02 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recognition', '0009_alter_audiofile_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofile',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
