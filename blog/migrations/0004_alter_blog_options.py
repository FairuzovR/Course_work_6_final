# Generated by Django 5.0.6 on 2024-06-21 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': [('can_edit_blog', 'Права на изменение блога'), ('can_delete_blog', 'Права на удаление блога'), ('can_add_blog', 'Права на добавление блога')], 'verbose_name': 'блог', 'verbose_name_plural': 'блоги'},
        ),
    ]