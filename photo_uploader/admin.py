from django.contrib import admin
from .models import Post,Media
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','caption','created_at')

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('post','file','get_user')
    
    def get_user(self, obj):
        return obj.post.user

    get_user.short_description = "User"

