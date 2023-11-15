# Generated by Django 4.2.6 on 2023-11-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_alter_vote_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='mark',
            field=models.IntegerField(choices=[('1', 'BAD'), ('5', 'NORMAL'), ('10', 'GOOD')], default='5'),
        ),
    ]