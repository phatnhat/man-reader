# Generated by Django 4.2.6 on 2023-11-06 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0023_view'),
    ]

    operations = [
        migrations.RenameField(
            model_name='view',
            old_name='view_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='view',
            name='view_count',
        ),
    ]
