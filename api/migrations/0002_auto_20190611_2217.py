# Generated by Django 2.2.1 on 2019-06-11 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='orders',
            field=models.ManyToManyField(blank=True, null=True, to='api.Order'),
        ),
    ]