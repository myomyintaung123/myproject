# Generated by Django 5.0.7 on 2024-08-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_bio_remove_profile_birth_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics'),
        ),
    ]
