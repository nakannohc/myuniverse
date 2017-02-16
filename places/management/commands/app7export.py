from django.core.management.base import BaseCommand, CommandError
import requests, json, xlwt


class Command(BaseCommand):
    help = '7 app'

    def handle(self, *args, **options):
        name = '7appexport'
        count = 0
        wb = xlwt.Workbook()
        ws = wb.add_sheet("sheet1")
        for i in range(1, 11077):
            sid = '%.5d' % i
            url = 'http://202.80.233.91/arcgis/rest/services/7App/MapServer/0/query?where=STORECODE%3D' + sid + '&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=OBJECTID%2CNAME%2C+LOCATION_T%2CSTORECODE%2CSTORENAME%2CZONE_CODE&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&f=pjson'
            req = requests.get(url)
            res = json.loads(req.content)
            if len(res['features']) > 0:
                ws.write(count, 0, res['features'][0]['attributes']['OBJECTID'])
                ws.write(count, 1, res['features'][0]['attributes']['STORENAME'])
                ws.write(count, 2, res['features'][0]['geometry']['x'])
                ws.write(count, 3, res['features'][0]['geometry']['y'])
                ws.write(count, 4, res['features'][0]['attributes']['STORECODE'])
                ws.write(count, 5, res['features'][0]['attributes']['LOCATION_T'])
                ws.write(count, 6, res['features'][0]['attributes']['Name'])
                ws.write(count, 7, res['features'][0]['attributes']['ZONE_CODE'])
                count += 1

        wb.save(name + '.xls')
