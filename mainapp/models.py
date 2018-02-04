from django.db import models
#from django.contrib import auth

class Performer(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userperformer')
    name_per = models.CharField(max_length=30)
    rating_per = models.IntegerField()
    image_per = models.CharField(max_length=50)
    about_per = models.TextField()
    date_per = models.DateField()

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
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='albumgenre')
    numplays_alb = models.IntegerField()
    rating_alb = models.IntegerField()
    image_alb = models.CharField(max_length=50)
    date_alb = models.DateField()

    def __str__(self):
        return self.name_alb

class Track(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    alb_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albumtrack')
    name_trc = models.CharField(max_length=50)
    gnr_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='trackgenre')
    link_trc = models.CharField(max_length=50)
    numplays_trc = models.IntegerField()
    rating_trc = models.IntegerField()

    def __str__(self):
        return self.name_trc

class LikedTrack(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='userliked')
    trc_id = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='trackliked')

    def __str__(self):
        return self.id








