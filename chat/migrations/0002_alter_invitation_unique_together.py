# Generated by Django 5.1.4 on 2024-12-17 13:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together={('sender', 'recipient', 'chatroom')},
        ),
    ]
