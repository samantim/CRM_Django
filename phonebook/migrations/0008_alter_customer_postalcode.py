# Generated by Django 4.2.2 on 2023-06-27 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebook', '0007_alter_customer_customertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='postalcode',
            field=models.CharField(max_length=10),
        ),
    ]