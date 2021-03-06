from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showgrid/?$', views.show_grid, name='show_grid'),
    url(r'^showplace/?$', views.show_place, name='show_place'),
    url(r'^exportexcel/?$', views.export_excel, name='export_excel'),
    url(r'^reportplace/?$', views.report_place, name='report_place'),
    url(r'^app7export/?$', views.app7_export, name='app7_export'),
    url(r'^gridstatus/?$', views.grid_status, name='grid_status'),
]
