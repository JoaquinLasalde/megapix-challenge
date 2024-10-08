# Generated by Django 5.1.1 on 2024-09-12 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('official_name', models.CharField(max_length=255)),
                ('flag_png', models.URLField()),
                ('flag_svg', models.URLField()),
                ('capital', models.CharField(blank=True, max_length=255, null=True)),
                ('population', models.BigIntegerField()),
                ('continent', models.CharField(max_length=255)),
                ('timezone', models.CharField(max_length=255)),
                ('area', models.FloatField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
    ]
