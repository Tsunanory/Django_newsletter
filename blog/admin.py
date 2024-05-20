from django.contrib import admin
from django.contrib.admin import ModelAdmin

from blog.models import Post


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', )
    search_fields = ('id', 'title', 'content', )
    # list_filter = ('is_active', )