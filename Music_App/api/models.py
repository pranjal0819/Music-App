from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Songs(models.Model):
    # id automatic generated in django
    title = models.CharField(max_length=200)
    url = models.URLField()
    duration = models.TimeField()

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


class PlayList(models.Model):
    # id automatic generated in django
    playlist_name = models.CharField(max_length=100)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Songs)

    def __str__(self):
        return self.playlist_name

    def as_dict(self):
        return {
            "id": self.id,
            "playlist_name": self.playlist_name,
            "song": [obj.as_dict() for obj in self.songs.all()]
        }


# This table automatic generate in many to many field in django
class SongsPlaylist(models.Model):
    fk_song = models.ForeignKey(Songs, on_delete=models.CASCADE, related_name='song')
    fk_playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE, related_name='playlist')
    sequence = models.IntegerField()

    def __str__(self):
        return self.sequence


class Schedule(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fk_user')
    fk_playlist = models.ForeignKey(PlayList, on_delete=models.CASCADE, related_name='fk_playlist')
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return self.scheduled_time
