import requests
import json
import time
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from places.models import Place, Grid

key = 'AIzaSyDq4qrtdYVQkr58iQi3s-Vm_RFslQdfcgE'


def get_detail(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    if res['status'] == 'OK':
        return res['result']
    else:
        return False


def radar_search(lat, lng, place_type, radius):
    url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' + lat + ',' + lng + '&radius=' + radius +'&type=' + place_type + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    if res['status'] == 'OK':
        return res['results']
    else:
        return False


def index(request):
    grids = Grid.objects.filter(scanned=False)
    for g in grids:
        places = radar_search(str(g.lat), str(g.lng), g.place_type, '5000')
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
        print g.id
        g.scanned = True
        g.save()
    return HttpResponse("Hello, world. You're at the polls index.")


def gen_grid(request):
    for i in range(0, 49):
        for j in range(0, 10):
            plng = i*0.094
            plat = j*0.090
            g = Grid(name='',
                     lat=13.45+plat,
                     lng=98.6+plng,
                     place_type='convenience_store')
            g.save()
    return HttpResponse("success")


def show_grid(request):
    grids = Grid.objects.all()
    return render(request, 'show_grid.html', {"grids": grids})
