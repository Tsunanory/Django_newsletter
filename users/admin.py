from django.contrib import admin

from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'email', )
    search_fields = ('email', 'id', )
    list_filter = ('is_active', )