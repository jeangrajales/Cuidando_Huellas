# Generated by Django 5.2 on 2025-05-28 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuidandoHuellas', '0019_categoriaticket_estadoticket_comentario_notificacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='estado',
            field=models.IntegerField(choices=[(1, 'Activo'), (0, 'Inhabilitado')], default=1),
        ),
        migrations.AddField(
            model_name='usuario',
            name='motivo_inhabilitacion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
