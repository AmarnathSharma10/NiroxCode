# Generated by Django 5.0.7 on 2024-07-23 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_submission_code_alter_coderunner_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coderunner',
            name='verdict',
            field=models.TextField(blank=True, null=True),
        ),
    ]
