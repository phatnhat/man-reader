# Generated by Django 4.2.6 on 2023-11-13 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0029_readinglist'),
        ('accounts', '0008_continuereading_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='continuereading',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books_continue_reading', to='book.book'),
        ),
        migrations.AlterField(
            model_name='continuereading',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapters_continue_reading', to='book.chapter'),
        ),
    ]