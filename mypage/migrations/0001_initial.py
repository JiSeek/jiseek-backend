# Generated by Django 4.0rc1 on 2021-12-07 07:39

import config.storages
import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('boards', '0001_initial'),
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, storage=config.storages.MediaStorage(), upload_to=core.utils.rename_imagefile_to_uuid)),
                ('board_favs', models.ManyToManyField(blank=True, related_name='board_favs', to='boards.Board')),
                ('food_favs', models.ManyToManyField(blank=True, related_name='food_favs', to='foods.Food')),
            ],
        ),
    ]
