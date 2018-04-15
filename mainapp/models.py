from django.db import models

class Performer(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userperformer')
    name_per = models.CharField(max_length=30, unique=True)
    rating_per = models.IntegerField(default=0)
    image_per = models.CharField(max_length=50, default='0')
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


class Album(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    per_id = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='performeralbum')
    name_alb = models.CharField(max_length=30)
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genrealbum')
    numplays_alb = models.IntegerField(default=0)
    rating_alb = models.IntegerField(default=0)
    image_alb = models.CharField(max_length=50, default='0')
    date_alb = models.DateField()
    slug = models.SlugField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name_alb


class Track(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    alb_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albumtrack')
    name_trc = models.CharField(max_length=50)
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genretrack')
    link_trc = models.CharField(max_length=50, default='')
    numplays_trc = models.IntegerField(default=0)
    rating_trc = models.IntegerField(default=0)
    date_trc = models.DateField()

    def __str__(self):
        return self.name_trc

    # def __str__(self):
    #     return "%s (%s)" % (
    #         self.name_trc,
    #         ", ".join(album.name_alb for album in self.alb_id),)


class LikedTrack(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userliked')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackliked')

    def __str__(self):
        return self.id
