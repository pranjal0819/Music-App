from django.urls import path

from .views import SongView, CreatePlayListView, AddSongToPlayListView, SongPlayListsView, ScheduleView

urlpatterns = [
    # path('add-song', SongView.as_view(), name='add_song'),
    path('song-list', SongView.as_view(), name='song_list'),

    path('create-playlist', CreatePlayListView.as_view(), name='create_playlist'),

    path('playlist', SongPlayListsView.as_view(), name='playlist'),

    path('add-song-to-playlist', AddSongToPlayListView.as_view(), name='add_song_to_playlist'),

    path('schedule-playlist', ScheduleView.as_view(), name='schedule_playlist'),
]
