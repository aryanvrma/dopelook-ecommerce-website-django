# Generated by Django 3.2.6 on 2021-08-29 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210829_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='Cash On delivery', max_length=100),
        ),
    ]