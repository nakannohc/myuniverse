# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from places.models import Place

class Command(BaseCommand):
    help = 'Dump Data'


    def migrate(size=500, start=0):
        count = Place.objects.using('myuniverse').count()
        print "%s objects in model %s" % (count, model)
        for i in range(start, count, size):
            print i,
            sys.stdout.flush()
            original_data =  Place.objects.using('postgres').all()[i:i+size]
            original_data_json = serializers.serialize("json", original_data)
            new_data = serializers.deserialize("json", original_data_json,
                                               using='default')
            for n in new_data:
                n.save(using='default')


    def handle(self, *args, **options):
        self.migrate()
