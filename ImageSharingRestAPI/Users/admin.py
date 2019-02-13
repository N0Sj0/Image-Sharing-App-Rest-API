from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    fields = ['username', 'image_url', 'firstname', 'lastname', 'bio', 'follows_string', 'followers_string']


admin.site.register(Profile, ProfileAdmin)