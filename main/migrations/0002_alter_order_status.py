# Generated by Django 4.1.4 on 2023-01-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Packing', 'Packing'), ('Waiting', 'Waiting for package collection'), ('Shipped', 'Shipped')], default='Packing', max_length=50),
        ),
    ]
