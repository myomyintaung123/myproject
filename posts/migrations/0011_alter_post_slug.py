# Generated by Django 5.0.7 on 2024-07-31 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_alter_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(),
        ),
    ]
