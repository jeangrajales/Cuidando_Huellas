# Generated by Django 5.1.1 on 2025-04-05 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuidandoHuellas', '0006_factura_detallefactura'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='DetalleFactura',
        ),
        migrations.DeleteModel(
            name='Factura',
        ),
    ]
