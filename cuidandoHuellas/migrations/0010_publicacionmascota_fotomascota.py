# Generated by Django 5.1.1 on 2025-04-05 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuidandoHuellas', '0009_detallefactura_delete_itemfactura'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicacionMascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_publicacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to='cuidandoHuellas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='FotoMascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='fotos_mascotas/')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='cuidandoHuellas.publicacionmascota')),
            ],
        ),
    ]
