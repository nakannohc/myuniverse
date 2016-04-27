# -*- coding: utf-8 -*-
import requests
import json
import xlwt
from django.db.models import Q
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
    url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location=' 
    url = url + lat + ',' + lng + '&radius=' + radius +'&type=' + place_type + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    if res['status'] == 'OK':
        return res['results']
    elif res['status'] == 'ZERO_RESULTS':
        return []
    else:
        #print res['status']
        return False


def text_search(lat, lng, query):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?radius=' 
    url = url + lat + ',' + lng + '&query=' + query + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    list = []
    #print url
    if res['status'] == 'OK':
        list += res['results']
        while 'next_page_token' in res:
            url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?radius='
            url = url + lat + ',' + lng + '&query=' + query + '&key=' + key + 'pagetoken=' + res['next_page_token']
            req = requests.get(url)
            res = json.loads(req.content)
            if res['status'] == 'OK':
                list += res['results']
        return list
    elif res['status'] == 'ZERO_RESULTS':
        return []
    else:
        #print res['status']
        return False


def nearby_search(lat, lng, radius, name):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    url = url + lat + ',' + lng + '&name=' + name + '&radius=' + radius + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    list = []
    #print url
    if res['status'] == 'OK':
        list += res['results']
        while 'next_page_token' in res:
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
            url = url + lat + ',' + lng + '&name=' + name + '&radius=' + radius + '&key=' + key + 'pagetoken=' + res['next_page_token']
            req = requests.get(url)
            res = json.loads(req.content)
            if res['status'] == 'OK':
                list += res['results']
        return list
    elif res['status'] == 'ZERO_RESULTS':
        return []
    else:
        #print res['status']
        return False
        

def index(request):
    not_scan = Grid.objects.filter(scanned=False).count()
    scan = Grid.objects.filter(scanned=True).count()

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


def show_grid(request):
    zone = request.GET.get('zone')
    if zone == 'all':
        grids = Grid.objects.all()
    else:
        grids = Grid.objects.filter(zone=zone)
    return render(request, 'show_grid.html', {"grids": grids})


def list_place(name):
    if name == '7eleven':
        places1 = Place.objects.filter(Q(name__icontains=u'7') & Q(name__icontains=u'eleven') & Q(place_type='convenience_store'))
        places2 = Place.objects.filter(Q(name__icontains=u'7') & Q(name__icontains=u'11') & Q(place_type='convenience_store'))
        places3 = Place.objects.filter(name__icontains=u'เซเ', place_type='convenience_store')
        places4 = Place.objects.filter(Q(name__icontains=u'7') & Q(name__icontains=u'eleven') & Q(place_type='shopping_mall'))
        places5 = Place.objects.filter(Q(name__icontains=u'7') & Q(name__icontains=u'11') & Q(place_type='shopping_mall'))
        places6 = Place.objects.filter(name__icontains='เซเ', place_type='shopping_mall')
        places = places1 | places2 | places3 | places4 | places5 | places6
        dl_link = '/places/exportexcel/?name=' + name
    elif name == 'srisawas':
        places1 = Place.objects.filter(name__icontains=u'เงิน', place_type='text_srisawas')
        places2 = Place.objects.filter(name__icontains=u'leas', place_type='text_srisawas')
        places3 = Place.objects.filter(name__icontains=u'ลิสซ', place_type='text_srisawas')
        places4 = Place.objects.filter(name__icontains=u'ลีสซ', place_type='text_srisawas')
        places = places1 | places2 | places3 | places4
        dl_link = '/places/exportexcel/?name=' + name
    elif name == 'nb7eleven':
        places = Place.objects.filter(place_type='nearby_7eleven')
    else:
        places = None
        dl_link = ''
    return places, dl_link


def report_place(request):
    name = request.GET.get('name')
    places, dl_link = list_place(name)
    return render(request, 'report_place.html', {"places": places, "dl_link": dl_link})


def export_excel(request):
    name = request.GET.get('name')
    places, dl_link = list_place(name)

    wb = xlwt.Workbook()

    #use xlwt to fill the workbook
    #
    ws = wb.add_sheet("sheet1")
    #ws.write(0, 0, "something")
    ws.write(0, 1, 'name')
    ws.write(0, 2, 'lat')
    ws.write(0, 3, 'lng')
    ws.write(0, 4, 'address')
    ws.write(0, 5, 'grid')
    row = 1
    for place in places:
        ws.write(row, 0, row)
        ws.write(row, 1, place.name)
        ws.write(row, 2, place.lat)
        ws.write(row, 3, place.lng)
        ws.write(row, 4, place.address)
        ws.write(row, 5, "%s (%f, %f)" % (place.grid.name, place.grid.lat, place.grid.lng))
        row += 1

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=' + name + '.xls'
    wb.save(response)
    return response

def show_place(request):
    name = request.GET.get('name')
    places, dl_link = list_place(name)

    return render(request, 'show_place.html', {"places": places})