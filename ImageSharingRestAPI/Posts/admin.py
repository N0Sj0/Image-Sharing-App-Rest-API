from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ['image_url', 'description', 'owner']


admin.site.register(Post, PostAdmin)