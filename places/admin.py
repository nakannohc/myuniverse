from django.contrib import admin
from .models import Place, Grid, KeywordSummary


class PlaceAdmin(admin.ModelAdmin):
    exclude = ('grid',)
    search_fields = ('name', 'place_id')

admin.site.register(Place, PlaceAdmin)
admin.site.register(Grid)
admin.site.register(KeywordSummary)


