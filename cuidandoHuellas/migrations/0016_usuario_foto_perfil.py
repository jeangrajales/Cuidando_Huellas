# Generated by Django 5.1.2 on 2025-05-01 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuidandoHuellas', '0015_alter_fotomascota_imagen_alter_producto_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='perfiles/'),
        ),
    ]
