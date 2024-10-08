# Generated by Django 5.0 on 2024-01-16 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_personalinfo_dob_alter_personalinfo_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="personalinfo",
            name="country_code",
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="first_name",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="gender",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="last_name",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name="personalinfo",
            name="portfolio_url",
            field=models.URLField(blank=True),
        ),
    ]
