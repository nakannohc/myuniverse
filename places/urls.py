from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gengrid/?$', views.gen_grid, name='gen_grid'),
    url(r'^showgrid/?$', views.show_grid, name='show_grid'),
    url(r'^showplace/?$', views.show_place, name='show_place'),
]
