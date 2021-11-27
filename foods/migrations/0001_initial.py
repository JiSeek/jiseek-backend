# Generated by Django 4.0rc1 on 2021-11-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('classification', models.CharField(max_length=40)),
                ('size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kcal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('moisture', models.DecimalField(decimal_places=2, max_digits=10)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carbohydrate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_sugar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dietary_fiber', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Ca', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Fe', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Mg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('P', models.DecimalField(decimal_places=2, max_digits=10)),
                ('K', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Na', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Zn', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Cu', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_D', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_K', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_B1', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_B2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_B12', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Vitamin_C', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amino_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('essential_amino_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Phenylalanine', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Cholesterol', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_essential_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_saturated_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_polyunsaturated_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Omega_3_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('trans_fatty_acids', models.DecimalField(decimal_places=2, max_digits=10)),
                ('folate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
