from django.db import models
from django.utils.timezone import now


class Performer(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='userperformer')
    name_per = models.CharField(max_length=30, unique=True)
    rating_per = models.IntegerField(default=0)
    image_per = models.FileField(default=None)
    about_per = models.TextField(null=True, blank=True)
    date_per = models.DateField(null=True, blank=True)
    slug = models.SlugField(max_length=30, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name_per


class Genre(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name_gnr = models.CharField(max_length=30)

    def __str__(self):
        return self.name_gnr


class GenreStyle(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genrestylegenre')
    name_stl = models.CharField(max_length=30)

    def __str__(self):
        return self.name_stl


class Album(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    per_id = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='albums')
    name_alb = models.CharField(max_length=60)
    stl_id = models.ForeignKey(GenreStyle, on_delete=models.CASCADE, related_name='style')
    numplays_alb = models.IntegerField(default=0)
    rating_alb = models.IntegerField(default=0)
    image_alb = models.FileField(upload_to='albums', default=None)
    date_alb = models.DateTimeField(default=now)
    about_alb = models.TextField(default='')
    slug = models.SlugField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name_alb


class Track(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    alb_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    name_trc = models.CharField(max_length=50)
    # stl_id = models.ForeignKey(GenreStyle, on_delete=models.CASCADE, related_name='genrestyletrack', default=None)
    audio_trc = models.FileField(upload_to='albums', default=None)
    numplays_trc = models.IntegerField(default=0)
    rating_trc = models.IntegerField(default=0)
    date_trc = models.DateField(default=now)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.name_trc


class LikedAlbum(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userlikedalbum')
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albumliked')
    date = models.DateField(default=now)

    def __int__(self):
        return self.id


class LikedTrack(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userliked')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackliked')
    date = models.DateField(default=now)

    def __int__(self):
        return self.id


class TrackHistory(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userhistory')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackhistory')

    def __int__(self):
        return self.trc_id


'''class TrackReport(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userreport')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackreport')

    def __int__(self):
        return self.trc_id'''


class Playlist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    per_id = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='playlistpreformer')
    title = models.CharField(max_length=60)
    image = models.FileField(default=None)

    def __str__(self):
        return self.title


class PlaylistTrack(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='pl_tracks')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackplaylist')

    def __int__(self):
        return self.id


class LikedPlaylist(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userlikedplaylist')
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlistliked')
    date = models.DateField(default=now)

    def __int__(self):
        return self.id


class TrackPlaysAmount(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackplays')
    date = models.DateField(default=now)
    amount = models.IntegerField(default=0)

    def __int__(self):
        return self.trc_id
