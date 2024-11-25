# Generated by Django 4.2.16 on 2024-11-24 12:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0004_orderitem"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Categoria", "verbose_name_plural": "Categorias"},
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name="customer",
            name="address",
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(max_length=500),
        ),
    ]
