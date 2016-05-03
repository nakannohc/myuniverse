from django.contrib import admin
from .models import Place, Grid


class PlaceAdmin(admin.ModelAdmin):
    exclude = ('grid',)

admin.site.register(Place, PlaceAdmin)
admin.site.register(Grid)


