# Generated by Django 5.0 on 2024-06-25 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobtype',
            name='type',
        ),
        migrations.AddField(
            model_name='jobtype',
            name='name',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
