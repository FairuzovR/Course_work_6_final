# Generated by Django 5.0.6 on 2024-06-21 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': [('can_view_blog', 'Can view blog'), ('can_edit_blog', 'Can edit blog'), ('can_delete_blog', 'Can delete blog')], 'verbose_name': 'блог', 'verbose_name_plural': 'блоги'},
        ),
    ]
