# -*- coding: utf-8 -*-
import urllib2
import bs4
import wget
import datetime
import pytz
import os
import sys
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Pantip 2G'

    def handle(self, *args, **options):

        mmonth = {u'ม.ค.': 1, u'ก.พ.':2, u'มี.ค.': 3, u'เม.ย.': 4,
                  u'พ.ค.': 5, u'มิ.ย.': 6, u'ก.ค.': 7, u'ส.ค.': 8,
                  u'ก.ย.': 9, u'ต.ค.': 10, u'พ.ย.': 11, u'ธ.ค.': 12,
                  u'\xb5.\xa4.': 10, u'\xe0\xc1.\xc2.': 4}
        dt = None
        old_dt = None

        last_page = 40

        for page in range(20, last_page+1):
            print '\r>> Page %d%%' % page,
            sys.stdout.flush()
            url = 'http://2g.pantip.com/cafe/rajdumnern/topicstockP.php?subgroup=&page=%d' % (page)

            req = urllib2.urlopen(url).read()
            req = str(req).decode('cp874')
            soup = bs4.BeautifulSoup(req, 'html.parser')

            dates = []
            p_links = []

            for dd in soup.find_all('font', {'color': '#C0C0C0'}):
                ll = dd.get_text().replace('PANTIP.COM', '').split(' ')
                ll = filter(None, ll)
                try:
                    day = int(ll[2])
                    month = mmonth[ll[3]]
                    year = int(ll[4])
                    hour = int(ll[5].split(':')[0])
                    minute = int(ll[5].split(':')[1].replace(')', ''))
                    dt = datetime.datetime(year=(year + 2500) - 543, month=month, day=day, hour=hour, minute=minute,
                                           tzinfo=pytz.utc)
                    old_dt = dt
                except:
                    raise
                    day = old_dt.day - 1
                    month = old_dt.month
                    year = int(ll[3])
                    hour = int(ll[4].split(':')[0])
                    minute = int(ll[4].split(':')[1].replace(')', ''))
                    dt = datetime.datetime(year=(year + 2500) - 543, month=month, day=day, hour=hour, minute=minute,
                                           tzinfo=pytz.utc)
                dates.append(dt)

            links = soup.find_all('a')
            for link in links:
                if 'rajdumnern' in link['href'] and 'topicstock' in link['href'] and 'html' in link['href']:
                    p_links.append(link['href'])
            #print len(p_links), len(dates)

            for i, link in enumerate(p_links):
                #print link
                try:
                    topic = urllib2.urlopen(link).read()
                except urllib2.HTTPError:
                    pass

                with open("pantip2g/pt_%s_pantip2g_%s" % (dates[i].strftime("%Y_%m_%d"), link.replace('http://topicstock.pantip.com/rajdumnern/', '').replace('/', '_')), "wb") as file:
                    file.write(topic)
                '''
                topic = bs4.BeautifulSoup(topic, 'html.parser')
                for script in topic(['script', 'style']):
                    script.extract()  # rip it out
                for font in topic.find_all('font', {'color': '#C0C080'}):
                    font.extract()
                for font in topic.find_all('font', {'color': '#F0F8FF'}):
                    font.extract()
                for font in topic.find_all('font', {'color': '#c0d3f3'}):
                    font.extract()
                for font in topic.find_all('font', {'color': '#E0E0E0'}):
                    if u'จากคุณ' in font.get_text():
                        font.extract()
                for font in topic.find_all('font', {'size': '-1'}):
                    font.extract()
                topic = topic.get_text().replace('\n', '').replace('\r', '')
                print topic
                '''
