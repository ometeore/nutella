# Generated by Django 2.2.5 on 2020-01-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_auto_20200122_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='aliment',
            field=models.ManyToManyField(blank=True, to='aliment.Aliment'),
        ),
    ]