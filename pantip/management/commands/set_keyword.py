# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from pantip.models import MarkTopic, Topic, TopicKeyword

class Command(BaseCommand):
    help = 'fix null kw'

    def handle(self, *args, **options):
        at = MarkTopic.objects.filter(p_keyword=None)[:5]
        print at.count()
        ct = TopicKeyword.objects.get(keyword=u'โกง')
        while(at.count()>0):
            at = MarkTopic.objects.filter(p_keyword=None)[:5]
            for t in at:
                t.p_keyword = ct
                t.save()
                
