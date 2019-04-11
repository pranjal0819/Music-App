from rest_framework import serializers

from .models import Songs, SongsPlaylist, PlayList, Schedule, UserTimeZone


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = '__all__'


class UserTimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTimeZone
        fields = ('time_zone',)


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('playlist_name',)


class SongsPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongsPlaylist
        fields = ('fk_song', 'fk_playlist')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('fk_playlist', 'scheduled_time')
