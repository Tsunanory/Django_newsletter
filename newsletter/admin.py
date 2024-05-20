from django.contrib import admin
from newsletter.models import Newsletter, Client, Message


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment', )
    search_fields = ('full_name', 'email', 'comment', )
    list_filter = ('email', )


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ('topic', 'content', )
    search_fields = ('topic', 'content', )
    list_filter = ('topic', )


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ('initial', 'frequency', )
    search_fields = ('message', 'client', 'initial', )
    list_filter = ('initial', )


