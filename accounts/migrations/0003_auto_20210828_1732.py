# Generated by Django 3.2.6 on 2021-08-28 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_staff',
            new_name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_superadmin',
        ),
    ]