# Generated by Django 5.0.6 on 2024-06-30 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
