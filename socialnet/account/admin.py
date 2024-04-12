from django.contrib import admin
from .models import Follow, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Follow)


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
