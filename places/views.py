# -*- coding: utf-8 -*-
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
    #print res['status']
    if res['status'] == 'OK':
        return res['result']
    elif res['status'] == 'ZERO_RESULTS':
        return []
    else:
        return False


def radar_search(lat, lng, place_type, radius):
    url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' + lat + ',' + lng + '&radius=' + radius +'&type=' + place_type + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    if res['status'] == 'OK':
        return res['results']
    elif res['status'] == 'ZERO_RESULTS':
        return []
    else:
        #print res['status']
        return False


def index(request):
    not_scan = len(Grid.objects.filter(scanned=False))
    scan = len(Grid.objects.filter(scanned=True))

    return HttpResponse("scanned: %d </br>not scan: %d <br>total: %d" % (scan, not_scan, scan+not_scan))


def put_mark(lat, lng, m, n, zone, place_type):
    count = 0
    for i in range(0, m):
        for j in range(0, n):
            g = Grid(name='%s %s %d, %d' % (zone, place_type, j, i),
                     lat=lat - j*0.034,
                     lng=lng + i*0.053+(j%2)*0.028,
                     place_type=place_type,
                     x=i,
                     y=j,
                     zone=zone)
            g.save()
            #print '.',
        count += 1
    return count


def gen_grid(request):
    put_mark(20.48, 99.0, 30, 20, 'north', 'convenience_store')
    put_mark(19.8, 97.26, 78, 70, 'north', 'convenience_store')
    put_mark(17.42, 98.1, 62, 92, 'central', 'convenience_store')
    put_mark(14.292, 98.577, 86, 26, 'central', 'convenience_store')
    put_mark(18.44, 101.394, 70, 70, 'northeast', 'convenience_store')
    put_mark(16.06, 101.394, 79, 52, 'northeast', 'convenience_store')
    put_mark(13.406, 100.432, 43, 27, 'east', 'convenience_store')
    put_mark(12.49, 101.997, 19, 30, 'east', 'convenience_store')
    put_mark(12.49, 101.997, 19, 30, 'east', 'convenience_store')
    put_mark(13.408, 99.107, 20, 50, 'south', 'convenience_store')
    put_mark(11.708, 99.107, 15, 22, 'south', 'convenience_store')
    put_mark(10.96, 98.206, 43, 100, 'south', 'convenience_store')
    put_mark(7.56, 99.001, 54, 33, 'south', 'convenience_store')
    put_mark(6.438, 100.778, 26, 26, 'south', 'convenience_store')
    return HttpResponse("success")


def show_grid(request):
    zone = request.GET.get('zone')
    grids = Grid.objects.all(zone=zone)
    return render(request, 'show_grid.html', {"grids": grids})


def show_place(request):
    places1 = Place.objects.filter(name__icontains=u'7')
    places2 = Place.objects.filter(name__icontains=u'เซ')
    places = places1 | places2
    return render(request, 'show_place.html', {"places": places})