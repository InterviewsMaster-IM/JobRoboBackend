# Generated by Django 5.0 on 2024-01-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resumes", "0003_coverletter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coverletter",
            name="file",
            field=models.FileField(upload_to="coverletters/"),
        ),
    ]
