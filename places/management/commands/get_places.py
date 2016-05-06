# -*- coding: utf-8 -*-
import time
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid
from places.views import get_detail, radar_search, text_search, nearby_search


class Command(BaseCommand):
    help = 'Parse places'

    def handle(self, *args, **options):
        numrows = 5
        grids = Grid.objects.filter(scanned=False)[:numrows]
        count_api = 0
        error = False
        while grids.count() and not error > 0:
            '''
            for g in grids:
                #print g.id,
                places = radar_search(str(g.lat), str(g.lng), g.place_type, '3000')
                #print places
                #print len(places)
                for place in places:
                    place_detail = get_detail(place['place_id'])
                    pp = Place.objects.filter(lat=place_detail['geometry']['location']['lat'],
                                              lng=place_detail['geometry']['location']['lng'])
                    if pp.count() == 0:
                        p = Place(name=place_detail['name'],
                                  place_type=place_type',
                                  lat=place_detail['geometry']['location']['lat'],
                                  lng=place_detail['geometry']['location']['lng'],
                                  address=place_detail['formatted_address'],
                                  grid=g)
                        p.save()
                #print '%s %f %f' % (place_detail['name'], place_detail['geometry']['location']['lat'], place_detail['geometry']['location']['lng'])
                #time.sleep(0.1)
                    #print '.',
                #print '.'
                g.scanned = True
                g.save()
            '''
            for g in grids:
                #print g.keyword,
                places, status = nearby_search(str(g.lat), str(g.lng), '3000', g.keyword)
                #print status
                if status == 'OVER_QUERY_LIMIT':
                    print '%s - OVER_QUERY_LIMIT' % time.strftime("%c")
                    error = True
                    break
                elif status == 'REQUEST_DENIED':
                    print '%s - REQUEST_DENIED' % time.strftime("%c")
                    error = True
                    break
                elif status == 'INVALID_REQUEST':
                    print '%s - INVALID_REQUEST' % time.strftime("%c")
                    error = True
                    break
                elif status == 'ZERO_RESULTS':
                    #print '%s - ZERO' % time.strftime("%c")
                    places = []
                elif status == 'OK':
                    count_api += 1
                    g.count_place = len(places)
                    #print places
                    #print len(places)
                    for place in places:
                        place_detail = get_detail(place['place_id'])
                        count_api += 1
                        pp = Place.objects.filter(lat=place_detail['geometry']['location']['lat'],
                                                  lng=place_detail['geometry']['location']['lng'],
                                                  grid__place_type=g.place_type)
                        if pp.count() == 0:
                            p = Place(name=place_detail['name'],
                                      lat=place_detail['geometry']['location']['lat'],
                                      lng=place_detail['geometry']['location']['lng'],
                                      address=place_detail['formatted_address'],
                                      grid=g)
                            p.save()
                g.scanned = True
                g.save()
            grids = Grid.objects.filter(scanned=False)[:numrows]
            if count_api > 149900:
                print count_api
                break

