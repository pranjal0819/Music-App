from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Songs, PlayList, Schedule
from .serializers import SongSerializer, PlayListSerializer, SongsPlaylistSerializer, ScheduleSerializer


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
        return Response(dictionaries)


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
        except TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ScheduleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data_list = Schedule.objects.filter(fk_user=request.user)
        serializer = ScheduleSerializer(data_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fk_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
