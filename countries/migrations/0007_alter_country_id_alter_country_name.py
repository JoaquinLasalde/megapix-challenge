# Generated by Django 5.1.1 on 2024-09-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0006_rename_continent_country_continents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
