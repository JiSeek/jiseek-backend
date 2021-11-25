# Generated by Django 4.0rc1 on 2021-11-23 04:50

from django.db import migrations, models
import mypage.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0001_initial'),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=mypage.utils.upload_image)),
                ('board_favs', models.ManyToManyField(blank=True, related_name='board_favs', to='boards.Board')),
                ('food_favs', models.ManyToManyField(blank=True, related_name='food_favs', to='foods.Food')),
            ],
        ),
    ]