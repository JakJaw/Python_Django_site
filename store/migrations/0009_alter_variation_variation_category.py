# Generated by Django 5.0.1 on 2024-02-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('kolor', 'kolor'), ('rozmiar', 'rozmiar'), ('podloze', 'podloze')], max_length=100, verbose_name='Variation category'),
        ),
    ]
