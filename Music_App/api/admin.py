from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Songs)
admin.site.register(PlayList)
admin.site.register(SongsPlaylist)
admin.site.register(Schedule)
admin.site.register(UserTimeZone)
