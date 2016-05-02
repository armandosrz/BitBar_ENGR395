from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'bitbars', 'hashed_password')
    list_filter = ['bitbars']

admin.site.register(User, UserAdmin)
