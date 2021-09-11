from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Notification

# Register your models here.
from website.models import UserProfile


class UserProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
