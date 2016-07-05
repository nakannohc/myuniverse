# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid, KeywordSummary, keywords
import xlwt

class Command(BaseCommand):
    help = 'Get logs'

    def handle(self, *args, **options):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('logs', cell_overwrite_ok=True)

        first_col = True
        col = 0
        for keyword in keywords:
            grids = Grid.objects.filter(keyword=keyword).order_by('zone', 'x', 'y')
            if first_col:
                row = 0
                ws.write(row, col, 'Grid')
                row += 1
                for grid in grids:
                    ws.write(row, col, '%s (%f, %f)' %(grid.zone, grid.lat, grid.lng))
                    row += 1
                col += 1
                first_col = False

            row = 0
            ws.write(row, col, keyword)
            row = 1
            for grid in grids:
                ws.write(row, col, grid.count_place)
                row += 1
            col += 1
            wb.save('task_log.xls')