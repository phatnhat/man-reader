# Generated by Django 4.2.6 on 2023-11-05 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='mark',
            field=models.IntegerField(choices=[('1', 'Bad'), ('5', 'Normal'), ('10', 'Good')], default='5'),
        ),
    ]