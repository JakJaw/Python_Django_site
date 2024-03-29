# Generated by Django 5.0.1 on 2024-01-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20231207_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(blank=True, upload_to='photos/categories/', verbose_name='Category Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=15, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='describtion',
            field=models.TextField(blank=True, max_length=255, verbose_name='Describtion'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Slug'),
        ),
    ]
