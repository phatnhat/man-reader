# Generated by Django 4.2.6 on 2023-10-24 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_book_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
