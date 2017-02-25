from django.contrib import admin
from .models import Topic, MarkTopic, TopicKeyword


class AdminTopic(admin.ModelAdmin):
    list_display = ['p_tid', 'p_name', 'p_keyword', 'p_datetime']

class AdminMarkTopic(admin.ModelAdmin):
    list_filter = ['read']
    list_display = ['p_tid', 'p_keyword', 'read']

admin.site.register(Topic, AdminTopic)
admin.site.register(TopicKeyword)
admin.site.register(MarkTopic, AdminMarkTopic)
