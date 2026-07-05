from django.contrib import admin
from .models import Blog,Comments,Reaction

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at', 'published')
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')

admin.site.register(Reaction)

