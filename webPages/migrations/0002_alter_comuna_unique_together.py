# Generated by Django 5.0.4 on 2024-05-07 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webPages', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comuna',
            unique_together={('nombre', 'region')},
        ),
    ]
