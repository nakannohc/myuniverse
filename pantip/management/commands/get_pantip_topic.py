# -*- coding: utf-8 -*-
import time, smtplib, requests, random
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from pantip.models import MarkTopic, Topic

class Command(BaseCommand):
    def __init__(self):
        self.pantip_url = 'http://search.pantip.com/'

    def set_params(self, keyword, room):
        self.params = {"ac": 0,
                  "q": keyword,
                  "r": room,
                  "s": "a",
                  "nms": "+Smart+Search+"}
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/53.0",
                   "X-Requested-With": "XMLHttpRequest"}

    help = 'Get Topic ID From Keyword'

    def handle(self, *args, **options):
        keywords = [u'โกง', u'โกงกิน', u'คอรัปชัน', u'คอรัปชั่น', u'corruption']
        for keyword in keywords:
            room = u'ราชดำเนิน'
            self.set_params(keyword, room)
            s_url = self.pantip_url+'/ss/'
            next = None

            while True:
                r = requests.get(s_url , params=self.params, headers=self.headers)
                # print r.content
                soup = BeautifulSoup(r.content, "lxml")
                links = soup.find_all('a')

                for link in links:
                    # print link['href']
                    if u'sr' in link['href']:
                        # print link['href']
                        r2 = requests.get(self.pantip_url + link['href'])
                        tid = int(r2.url.split('/')[4])
                        print tid
                        try:
                            mt = MarkTopic.objects.get(p_tid=tid)
                        except MarkTopic.DoesNotExist:
                            mt = None

                        if mt is None:
                            mt = MarkTopic(p_tid=tid)
                            mt.save()
                    if u'ถัดไป' in link.text:
                        next = link['href']
                        s_url = self.pantip_url + next
                        print s_url,
                    else:
                        next = None

                if next is None:
                    break

