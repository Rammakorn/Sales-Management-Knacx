# Generated by Django 5.1.6 on 2025-02-08 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.IntegerField(db_column='product_id', primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50)),
            ],
        ),
    ]
