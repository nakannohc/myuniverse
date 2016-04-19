from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid
from places.views import get_detail, radar_search


class Command(BaseCommand):
    help = 'Parse places'

    def handle(self, *args, **options):
        grids = Grid.objects.filter(scanned=False)
        print 'ddd'
        for g in grids:
            print g.id,
            places = radar_search(str(g.lat), str(g.lng), g.place_type, '5000')
            #print places
            #print len(places)
            for place in places:
                place_detail = get_detail(place['place_id'])
                pp = Place.objects.filter(lat=place_detail['geometry']['location']['lat'],
                                          lng=place_detail['geometry']['location']['lng'])
                if pp.count() == 0:
                    p = Place(name=place_detail['name'],
                              place_type='convenience_store',
                              lat=place_detail['geometry']['location']['lat'],
                              lng=place_detail['geometry']['location']['lng'])
                    p.save()
            #print '%s %f %f' % (place_detail['name'], place_detail['geometry']['location']['lat'], place_detail['geometry']['location']['lng'])
            #time.sleep(0.1)
                print '.',
            print '.'
            g.scanned = True
            g.save()