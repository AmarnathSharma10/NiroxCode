# Generated by Django 5.0.7 on 2024-07-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_active_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=12),
        ),
    ]
