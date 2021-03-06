# Generated by Django 2.0.8 on 2019-02-15 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('_id', models.IntegerField(primary_key=True, serialize=False)),
                ('id', models.IntegerField(primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=5)),
                ('imdb_id', models.CharField(max_length=10)),
                ('genre', models.CharField(max_length=100)),
                ('movie_logo', models.CharField(max_length=300)),
                ('imdb_rating', models.FloatField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('release_date', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashid', models.CharField(max_length=200, unique=True)),
                ('user', models.CharField(max_length=100)),
                ('movie', models.CharField(max_length=50)),
                ('rating', models.FloatField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
