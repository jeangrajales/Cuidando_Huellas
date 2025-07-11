# Generated by Django 5.2 on 2025-05-25 21:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuidandoHuellas', '0018_rename_resuelto_reporte_revisado_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Categoría de Ticket',
                'verbose_name_plural': 'Categorías de Tickets',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='EstadoTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(help_text='Código de color CSS (ej: bg-warning)', max_length=20)),
                ('orden', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Estado de Ticket',
                'verbose_name_plural': 'Estados de Tickets',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='comentarios/')),
                ('fecha_comentario', models.DateTimeField(auto_now_add=True)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='cuidandoHuellas.publicacionmascota')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuidandoHuellas.usuario')),
            ],
            options={
                'db_table': 'comentarios',
                'ordering': ['-fecha_comentario'],
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('comentario', 'Comentario'), ('publicacion', 'Publicación')], max_length=20)),
                ('titulo', models.CharField(max_length=255)),
                ('mensaje', models.TextField()),
                ('leida', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cuidandoHuellas.comentario')),
                ('publicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cuidandoHuellas.publicacionmascota')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to='cuidandoHuellas.usuario')),
            ],
            options={
                'db_table': 'notificaciones',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='PreguntaFrecuente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=255)),
                ('respuesta', models.TextField()),
                ('activo', models.BooleanField(default=True)),
                ('orden', models.PositiveSmallIntegerField(default=0)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='preguntas_frecuentes', to='cuidandoHuellas.categoriaticket')),
            ],
            options={
                'verbose_name': 'Pregunta Frecuente',
                'verbose_name_plural': 'Preguntas Frecuentes',
                'ordering': ['orden', 'pregunta'],
            },
        ),
        migrations.CreateModel(
            name='TicketSoporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_ticket', models.CharField(editable=False, max_length=20, unique=True)),
                ('asunto', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('prioridad', models.CharField(choices=[('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta'), ('urgente', 'Urgente')], default='media', max_length=10)),
                ('archivo_adjunto', models.FileField(blank=True, null=True, upload_to='soportes/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuidandoHuellas.categoriaticket')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='cuidandoHuellas.estadoticket')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ticket de Soporte',
                'verbose_name_plural': 'Tickets de Soporte',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='RespuestaTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('archivo_adjunto', models.FileField(blank=True, null=True, upload_to='soportes/respuestas/')),
                ('es_respuesta_admin', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='cuidandoHuellas.ticketsoporte')),
            ],
            options={
                'verbose_name': 'Respuesta de Ticket',
                'verbose_name_plural': 'Respuestas de Tickets',
                'ordering': ['fecha_creacion'],
            },
        ),
    ]
