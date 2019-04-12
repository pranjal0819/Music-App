import pytz
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from .models import Songs, PlayList, Schedule, UserTimeZone
from .serializers import SongSerializer, PlayListSerializer, SongsPlaylistSerializer, ScheduleSerializer
from .serializers import UserTimeZoneSerializer


# Create your views here.

class SongView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        song_list = Songs.objects.all()
        # dictionaries = [obj.as_dict() for obj in song_list]
        serializer = SongSerializer(song_list, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = SongSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeZoneView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data['time_zone']
            if data in pytz.all_timezones_set:
                try:
                    obj = UserTimeZone.objects.get(user=request.user)
                    obj.time_zone = data
                    obj.save(update_fields=['time_zone'])
                except ObjectDoesNotExist:
                    obj = UserTimeZone.objects.create(time_zone=data, user=request.user)
                serializer = UserTimeZoneSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Invalid Timezone", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Provide Timezone", status=status.HTTP_400_BAD_REQUEST)


class CreatePlayListView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PlayListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fk_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# noinspection PyBroadException
class SongPlayListsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        obj_list = PlayList.objects.filter(fk_user=request.user)
        dictionaries = [obj.as_dict() for obj in obj_list]
        return Response(dictionaries, status=status.HTTP_200_OK)


# noinspection PyBroadException
class AddSongToPlayListView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            serializer = SongsPlaylistSerializer(data=request.data)
            if serializer.is_valid():
                obj = PlayList.objects.get(id=request.data['fk_playlist'], fk_user=request.user)
                song = Songs.objects.get(id=request.data['fk_song'])
                obj.songs.add(song)
                dictionaries = [obj.as_dict()]
                return Response(dictionaries)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Invalid Primary Key', status=status.HTTP_400_BAD_REQUEST)


class ScheduleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            time_zone = request.user.usertimezone.time_zone
        except Exception:
            time_zone = settings.TIME_ZONE
        zone = pytz.timezone(time_zone)
        data_list = Schedule.objects.filter(fk_user=request.user)
        my_obj_list = []
        for obj in data_list:
            my_obj_list.append({
                "fk_playlist": obj.fk_playlist.playlist_name,
                "scheduled_time": obj.scheduled_time.astimezone(zone).strftime('%Y-%m-%dT%H:%M:%S')
            })
        return Response(my_obj_list, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    time_zone = request.user.usertimezone.time_zone
                except Exception:
                    time_zone = settings.TIME_ZONE
                playlist_obj = PlayList.objects.get(id=request.data['fk_playlist'], fk_user=request.user)

                datetime_obj = datetime.datetime.strptime(request.data['scheduled_time'], "%Y-%m-%dT%H:%M:%S")
                date_time = datetime_obj.replace(tzinfo=pytz.timezone(time_zone))
                # print(date_time)
                Schedule.objects.create(fk_playlist=playlist_obj, scheduled_time=date_time, fk_user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response("Forbidden", status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response("Date Time does not match format \'%Y-%m-%d %H:%M:%S\'", status.HTTP_403_FORBIDDEN)
