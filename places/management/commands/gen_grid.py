# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid, keywords
from places.views import get_detail, radar_search, put_mark
import xlrd


class Command(BaseCommand):
    help = 'Gen grids'

    def handle(self, *args, **options):

        # not use now
        wb = xlrd.open_workbook('keywords.xlsx')
        ws = wb.sheet_by_index(1)

        for i in range(0, ws.nrows):
            kw = ws.cell_value(i, 0)
            pt = ws.cell_value(i, 1)

            place_type = pt
            keyword = kw
            g = Grid.objects.filter(place_type=place_type, keyword=keyword)
            g.delete()

        for i in range(0, ws.nrows):
            kw = ws.cell_value(i, 0)
            pt = ws.cell_value(i, 1)
            print kw, pt

            place_type = pt
            keyword = kw

            put_mark(20.48, 99.0, 30, 20, 'north 1', place_type, keyword)
            put_mark(19.8, 97.26, 78, 70, 'north 2', place_type, keyword)
            put_mark(17.42, 98.1, 62, 92, 'central 1', place_type, keyword)
            put_mark(14.292, 98.577, 86, 26, 'central 2', place_type, keyword)
            put_mark(18.44, 101.394, 70, 70, 'northeast 1', place_type, keyword)
            put_mark(16.06, 101.394, 79, 52, 'northeast 2', place_type, keyword)
            put_mark(13.406, 100.432, 43, 27, 'east 1', place_type, keyword)
            put_mark(12.49, 101.997, 19, 30, 'east 2', place_type, keyword)
            put_mark(12.49, 101.997, 19, 30, 'east 3', place_type, keyword)
            put_mark(13.408, 99.107, 20, 50, 'south 1', place_type, keyword)
            put_mark(11.708, 99.107, 15, 22, 'south 2', place_type, keyword)
            put_mark(10.96, 98.206, 43, 100, 'south 3', place_type, keyword)
            put_mark(7.56, 99.001, 54, 33, 'south 4', place_type, keyword)
            put_mark(6.438, 100.778, 26, 26, 'south 5', place_type, keyword)
            #print count

        