# Generated by Django 5.0.6 on 2024-06-21 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
