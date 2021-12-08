# Generated by Django 4.0rc1 on 2021-12-07 16:49

import config.storages
import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, storage=config.storages.MediaStorage(), upload_to=core.utils.rename_imagefile_to_uuid),
        ),
    ]
