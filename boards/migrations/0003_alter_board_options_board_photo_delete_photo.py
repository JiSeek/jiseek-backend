# Generated by Django 4.0rc1 on 2021-11-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='board',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
