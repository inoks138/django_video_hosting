# Generated by Django 4.0.4 on 2022-05-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_episode_video_alter_film_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='type',
            field=models.CharField(choices=[('film', 'film'), ('animation', 'animation'), ('all', 'all')], default='all', max_length=10),
        ),
        migrations.AddField(
            model_name='movie',
            name='is_animation',
            field=models.BooleanField(default=False, verbose_name='Мультфильм'),
        ),
    ]
