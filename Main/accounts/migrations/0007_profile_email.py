# Generated by Django 5.0.7 on 2024-07-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
