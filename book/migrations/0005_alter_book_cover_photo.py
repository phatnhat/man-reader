# Generated by Django 4.2.6 on 2023-10-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_photo',
            field=models.FileField(blank=True, null=True, upload_to='https://api.imgbb.com/1/upload'),
        ),
    ]