# Generated by Django 2.0.1 on 2018-02-07 03:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_alb', models.CharField(max_length=30)),
                ('numplays_alb', models.IntegerField(default=0)),
                ('rating_alb', models.IntegerField(default=0)),
                ('image_alb', models.CharField(default='0', max_length=50)),
                ('date_alb', models.DateField()),
                ('slug', models.SlugField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_gnr', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LikedTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_per', models.CharField(max_length=30, unique=True)),
                ('rating_per', models.IntegerField(default=0)),
                ('image_per', models.CharField(default='0', max_length=50)),
                ('about_per', models.TextField(blank=True, null=True)),
                ('date_per', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=30, null=True, unique=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userperformer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_trc', models.CharField(max_length=50)),
                ('link_trc', models.CharField(max_length=50)),
                ('numplays_trc', models.IntegerField(default=0)),
                ('rating_trc', models.IntegerField(default=0)),
                ('date_trc', models.DateField()),
                ('alb_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albumtrack', to='mainapp.Album')),
                ('gnr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackgenre', to='mainapp.Genre')),
            ],
        ),
        migrations.AddField(
            model_name='likedtrack',
            name='trc_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackliked', to='mainapp.Track'),
        ),
        migrations.AddField(
            model_name='likedtrack',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userliked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='gnr_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albumgenre', to='mainapp.Genre'),
        ),
        migrations.AddField(
            model_name='album',
            name='per_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performeralbum', to='mainapp.Performer'),
        ),
    ]
