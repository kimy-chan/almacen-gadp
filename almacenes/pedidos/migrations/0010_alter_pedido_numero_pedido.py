# Generated by Django 5.0.3 on 2024-08-19 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0009_alter_pedido_numero_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='numero_pedido',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
