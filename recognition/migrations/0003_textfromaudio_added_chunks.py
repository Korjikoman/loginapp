# Generated by Django 4.2.15 on 2025-02-24 09:44

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recognition', '0002_remove_audiofile_file_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='textfromaudio',
            name='added',
            field=models.TimeField(default=datetime.datetime(2025, 2, 24, 9, 44, 22, 346302, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Chunks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chunk', models.FileField(null=True, upload_to='AudioChunks/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['wav', 'mp3', 'aac', 'flac', 'ogg'])])),
                ('uploaded', models.TimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
