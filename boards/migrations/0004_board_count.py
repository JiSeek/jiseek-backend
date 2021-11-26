# Generated by Django 4.0rc1 on 2021-11-26 10:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0003_alter_board_options_board_photo_delete_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='count',
            field=models.ManyToManyField(related_name='boards_count', to=settings.AUTH_USER_MODEL),
        ),
    ]
