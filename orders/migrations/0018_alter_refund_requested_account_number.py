# Generated by Django 3.2.6 on 2021-08-30 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_order_refund_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund_requested',
            name='Account_Number',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
