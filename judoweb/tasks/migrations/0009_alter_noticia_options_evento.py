# Generated by Django 5.0.4 on 2024-05-25 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_pdf_estado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticia',
            options={'ordering': ['-fecha_publicacion']},
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.pdf')),
            ],
        ),
    ]
