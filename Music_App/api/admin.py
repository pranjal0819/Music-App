from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

# Register your models here.
admin.site.register(Songs)
admin.site.register(PlayList)
admin.site.register(SongsPlaylist)
admin.site.register(Schedule)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserTimezoneInline(admin.StackedInline):
    model = UserTimeZone
    can_delete = True
    verbose_name_plural = 'time_zone'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserTimezoneInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
