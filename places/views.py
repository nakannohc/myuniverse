# -*- coding: utf-8 -*-
import requests
import json
import xlwt
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from places.models import Place, Grid

key = 'AIzaSyDq4qrtdYVQkr58iQi3s-Vm_RFslQdfcgE'
keywords = [u'ธนาคาร',  u'ATM',  u'CDM',  u'บริษัทเงินทุน',  u'บริษัทเครดิตฟองซิเอร์',
            u'บริษัทหลักทรัพย์',  u'ออมสิน',  u'ธกส',  u'ธอส',  u'ธสน',  u'ธนาคารอิสลาม',
            u'SME Bank',  u'ประกัน',  u'แคปปิตอล โอเค',  u'เจเนอรัล คาร์ด เซอร์วิสเซส',
            u'ซิตี้ คอนซูเมอร์',  u'เทสโก้ คาร์ด',  u'บัตรกรุงไทย',  u'บัตรกรุงศรีอยุธยา',
            u'อยุธยา แคปปิตอล',  u'อิออน ธนสินทรัพย์',  u'อีซี่บาย',  u'ลิสซิ่ง',  u'แฟคตอริ่ง',
            u'กรุงไทยธุรกิจลีสซิ่ง',  u'แคปปิตอล โอเค',  u'เงินติดล้อ',  u'เงินสดทันใจ',
            u'จี แคปปิตอล',  u'เจ เอ็ม ที เน็ทเวอร์ค เซอร์วิสเซ็ส',  u'เจ เอ็ม ที พลัส',
            u'เจเนอรัล คาร์ด เซอร์วิสเซส',  u'ซิงเกอร์ประเทศไทย',  u'ซิตี้คอร์ป ลิสซิ่ง(ประเทศไทย)',
            u'ไซเบอร์เนตติคส์',  u'โตโยต้าลิสซิ่ง',  u'เทสโก้ คาร์ด เซอร์วิสเซส',  u'ไทยพาณิชย์ลีสซิ่ง',
            u'ไทยเอซ แคปปิตอล',  u'บัตรกรุงไทย',  u'บัตรกรุงศรีอยุธยา',  u'พรอมิส (ประเทศไทย)',
            u'มีนาลิสซิ่ง',  u'เมืองไทย ลิสซิ่ง',  u'แมคคาเล กรุ๊พ',  u'รีโซลูชั่น เวย์',  u'วัฒนาธนวินทรัพย์',
            u'วี แคช เอ็นเตอร์ไพรส์',  u'ศักดิ์สยามพาณิชย์ลิสซิ่ง',  u'สยามเจเนอรัลแฟคตอริ่ง',  u'สินมิตร',
            u'อยุธยา แคปปิตอล เซอร์วิสเซส',  u'อยุธยา แคปปิตอล ออโต้ ลีส',  u'อินเทลลิเจนท์ ทีที. พาวเวอร์',
            u'อิออน ธนสินทรัพย์ (ไทยแลนด์)',  u'อีซี่ บาย',  u'เอเซียเสริมกิจลีสซิ่ง',  u'ไอร่า แอนด์ ไอฟุล',
            u'เงินติดล้อ',  u'เงินสดทันใจ',  u'โดเมสติค แคปปิตอล 2015',  u'ทีเค เงินสดทันใจ',
            u'ไทยเอช แคปปิตอล',  u'ปิยะระยองกรุ๊ป',  u'พี.เอส.เอ็น.ลีสซิ่ง',  u'มีนาลีสซิ่ง',
            u'เมืองไทย ลีสซิ่ง',  u'แมคคาเล กรุ๊พ',  u'ไมด้า ลีสซิ่ง',  u'สหไพบูลย์(2558)',
            u'อินเทลลิเจนท์ ทีที พาวเวอร์',  u'พสิษฐ์ภาคิณ',  u'สหกรณ์',  u'กลุ่มเกษตกร',  u'กลุ่มอาชีพ',
            u'กองทุนหมู่บ้าน',  u'ออมทรัพย์เพื่อการผลิต',  u'การเงินชุมชน',  u'กลุ่มสัจจะ',  u'family mart',
            u'max valu',  u'max value',  u'108 shop',  u'cp freshmart',  u'บิ๊กซี',  u'เทสโก้',
            u'makro',  u'ห้างสรรพสินค้า',  u'ศูนย์การค้า',  u'ไปรษณีย์',  u'AIS',  u'telewiz',  u'เทเลวิซ',
            u'ทรูช็อป',  u'Dtac',  u'ดีแทค',  u'ศูนย์บริการ ทีโอที',  u'ศูนย์บริการ TOT',  u'เจมาร์ท',
            u'ปั๊มน้ำมัน',  u'ตู้เติมเงิน']


def get_detail(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&key=' + key
    req = requests.get(url)
    res = json.loads(req.content)
    #print res['status']
    err_message = ''
    if res['status'] == 'OK':
        return res['result'], 'OK', err_message
    elif res['status'] == 'ZERO_RESULTS':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'ZERO_RESULTS', err_message
    elif res['status'] == 'OVER_QUERY_LIMIT':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'OVER_QUERY_LIMIT', err_message
    elif res['status'] == 'REQUEST_DENIED':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'REQUEST_DENIED', err_message
    elif res['status'] == 'INVALID_REQUEST':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'INVALID_REQUEST', err_message
    else:
        if 'error_message' in res:
            err_message = res['error_message']
        return [], res['status'], err_message


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
    err_message = ''
    if res['status'] == 'OK':
        list += res['results']
        while 'next_page_token' in res:
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
            url = url + lat + ',' + lng + '&name=' + name + '&radius=' + radius + '&key=' + key + 'pagetoken=' + res['next_page_token']
            req = requests.get(url)
            res = json.loads(req.content)
            if res['status'] == 'OK':
                list += res['results']
        return list, 'OK', err_message
    elif res['status'] == 'ZERO_RESULTS':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'ZERO_RESULTS', err_message
    elif res['status'] == 'OVER_QUERY_LIMIT':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'OVER_QUERY_LIMIT', err_message
    elif res['status'] == 'REQUEST_DENIED':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'REQUEST_DENIED', err_message
    elif res['status'] == 'INVALID_REQUEST':
        if 'error_message' in res:
            err_message = res['error_message']
        return [], 'INVALID_REQUEST', err_message
    else:
        if 'error_message' in res:
            err_message = res['error_message']
        return [], res['status'], err_message
        

def index(request):
    not_scan = Grid.objects.filter(scanned=False).count()
    scan = Grid.objects.filter(scanned=True).count()
    list_keywords = []

    for keyword in keywords:
        d = {}
        d['keyword'] = keyword
        d['link'] = '/places/exportexcel/?name=' + keyword
        d['notcomplete'] = Grid.objects.filter(scanned=False, keyword=keyword).count()
        d['complete'] = Grid.objects.filter(scanned=True, keyword=keyword).count()
        d['total'] = d['notcomplete'] + d['complete']
        list_keywords.append(d)

    return render(request, 'searchreport.html',
                  {"keywords": list_keywords,
                   'allscan': scan,
                   'allnotscan': not_scan,
                   'all': scan + not_scan})


@csrf_protect
def grid_status(request):
    k = request.POST.get('keyword')
    d = {}
    d['keyword'] = k
    ncm = Grid.objects.filter(keyword=k, scanned=False).count()
    cm = Grid.objects.filter(keyword=k, scanned=True).count()
    d['notcomplete'] = ncm
    d['complete'] = cm
    d['total'] = ncm+cm
    d['link'] = '/places/exportexcel/?name=' + k
    #print d
    return HttpResponse(json.dumps(d))


def put_mark(lat, lng, m, n, zone, place_type, keyword):
    count = 0
    for i in range(0, m):
        for j in range(0, n):
            g = Grid(name='%s %s %d, %d' % (zone, place_type, j, i),
                     lat=lat - j*0.034,
                     lng=lng + i*0.053+(j%2)*0.028,
                     place_type=place_type,
                     x=i,
                     y=j,
                     keyword=keyword,
                     count_place=0,
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
        dl_link = 'nb7eleven'
    else:
        places = Place.objects.filter(grid__keyword=name)
        dl_link = '/places/exportexcel/?name=' + name
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
    response['Content-Disposition'] = 'attachment; filename=' + 'exportdata' + '.xls'
    wb.save(response)
    return response


def show_place(request):
    name = request.GET.get('name')
    places, dl_link = list_place(name)

    return render(request, 'show_place.html', {"places": places})


def app7_export(request):
    name = '7appexport'
    count = 0
    wb = xlwt.Workbook()
    ws = wb.add_sheet("sheet1")
    for i in range(1, 6):
        sid = '%.5d' % i
        url = 'http://202.80.233.91/arcgis/rest/services/7App/MapServer/0/query?where=STORECODE%3D' + sid + '&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=OBJECTID%2CNAME%2C+LOCATION_T%2CSTORECODE%2CSTORENAME%2CZONE_CODE&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&f=pjson'
        req = requests.get(url)
        res = json.loads(req.content)
        if len(res['features']) > 0:
            ws.write(i, 0, res['features'][0]['attributes']['OBJECTID'])
            ws.write(i, 1, res['features'][0]['attributes']['STORENAME'])
            ws.write(i, 2, res['features'][0]['geometry']['x'])
            ws.write(i, 3, res['features'][0]['geometry']['y'])
            ws.write(i, 4, res['features'][0]['attributes']['STORECODE'])
            ws.write(i, 5, res['features'][0]['attributes']['LOCATION_T'])
            ws.write(i, 6, res['features'][0]['attributes']['Name'])
            ws.write(i, 7, res['features'][0]['attributes']['ZONE_CODE'])
            count += 1

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=' + name + '.xls'
    wb.save(response)
    return response
