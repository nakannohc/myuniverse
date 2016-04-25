from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid
from places.views import get_detail, radar_search, put_mark


class Command(BaseCommand):
    help = 'Gen grids'

    def handle(self, *args, **options):
	    place_type = 'text_srisawas'    	    
        g = Grid.objects.filter(place_type=place_type)
        g.delete()
        put_mark(20.48, 99.0, 30, 20, 'north', place_type)
        put_mark(19.8, 97.26, 78, 70, 'north', place_type)
        put_mark(17.42, 98.1, 62, 92, 'central', place_type)
        put_mark(14.292, 98.577, 86, 26, 'central', place_type)
        put_mark(18.44, 101.394, 70, 70, 'northeast', place_type)
        put_mark(16.06, 101.394, 79, 52, 'northeast', place_type)
        put_mark(13.406, 100.432, 43, 27, 'east', place_type)
        put_mark(12.49, 101.997, 19, 30, 'east', place_type)
        put_mark(12.49, 101.997, 19, 30, 'east', place_type)
        put_mark(13.408, 99.107, 20, 50, 'south', place_type)
        put_mark(11.708, 99.107, 15, 22, 'south', place_type)
        put_mark(10.96, 98.206, 43, 100, 'south', place_type)
        put_mark(7.56, 99.001, 54, 33, 'south', place_type)
        put_mark(6.438, 100.778, 26, 26, 'south', place_type)
        #print count
