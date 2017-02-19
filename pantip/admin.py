from django.contrib import admin
from .models import Topic, MarkTopic


class AdminMarkTopic(admin.ModelAdmin):
    list_filter = ['read']

admin.site.register(Topic)
admin.site.register(MarkTopic, AdminMarkTopic)
