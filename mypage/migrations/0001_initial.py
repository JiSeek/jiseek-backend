# Generated by Django 4.0b1 on 2021-11-17 13:59

from django.db import migrations, models
import mypage.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=mypage.utils.upload_image)),
                ('nickname', models.CharField(max_length=30, null=True, unique=True)),
            ],
        ),
    ]
