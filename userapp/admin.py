from django.contrib import admin

# Register your models here.
from userapp.models import User


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserProfileAdmin)
