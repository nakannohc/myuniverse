# -*- coding: utf-8 -*-
import time
import smtplib
import json
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid, KeywordSummary, keywords
from places.views import get_detail, radar_search, text_search, nearby_search



class Command(BaseCommand):
    help = 'Parse places'

    def send_email(self, message):
        gmail_user = 'nakannohc@gmail.com'
        gmail_pwd = 'qTut0L2$'
        FROM = 'nakannohc@gmail.com'
        TO = 'chonnakan.r@gmail.com'
        SUBJECT = 'Message from GIS server %s' % time.strftime("%c")
        TEXT = message

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, TO, SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            #print 'successfully sent the mail'
        except:
            #raise
            print "failed to send mail"

    def handle(self, *args, **options):
        self.send_email('Start Search Places - %s' % time.strftime("%c"))
        error = False
        numrows = 10
        count_api = 0
        for keyword in keywords:
            grids = Grid.objects.filter(scanned=False, keyword=keyword)[:numrows]
            while grids.count() and not error > 0:
                for g in grids:
                    #print g.keyword,
                    places, status, err_message = nearby_search(str(g.lat), str(g.lng), '3000', g.keyword)
                    #print status
                    if status == 'OVER_QUERY_LIMIT':
                        print '%s - OVER_QUERY_LIMIT - %s' % (time.strftime("%c"), err_message)
                        self.send_email('OVER_QUERY_LIMIT')
                        error = True
                        break
                    elif status == 'REQUEST_DENIED':
                        print '%s - REQUEST_DENIED - %s' % (time.strftime("%c"), err_message)
                        self.send_email('REQUEST_DENIED')
                        #error = True
                        #break
                    elif status == 'INVALID_REQUEST':
                        print '%s - INVALID_REQUEST- %s' % (time.strftime("%c"), err_message)
                        self.send_email('INVALID_REQUEST')
                        #error = True
                        #break
                    elif status == 'ZERO_RESULTS':
                        #print '%s - ZERO' % time.strftime("%c")
                        places = []
                    elif status == 'OK':
                        count_api += 1
                        g.count_place = len(places)
                        #print places
                        #print len(places)
                        for place in places:
                            place_detail, status, err_message = get_detail(place['place_id'])
                            count_api += 1
                            pp = Place.objects.filter(lat=place_detail['geometry']['location']['lat'],
                                                      lng=place_detail['geometry']['location']['lng'],
                                                      grid__place_type=g.place_type)
                            if pp.count() == 0:
                                p = Place(name=place_detail['name'],
                                          lat=place_detail['geometry']['location']['lat'],
                                          lng=place_detail['geometry']['location']['lng'],
                                          address=place_detail['formatted_address'],
                                          grid=g,
                                          place_id=place_detail['place_id'],
                                          place_detail=json.dumps(place_detail))

                                if 'permanently_closed' in place_detail:
                                    p.permanently_closed = True
                                else:
                                    p.permanently_closed = False
                                p.save()
                        kws = KeywordSummary.objects.get(keyword=g.keyword)
                        kws.grid_complete += 1
                        g.scanned = True
                        kws.save()
                        g.save()
                    else:
                        print status + ' - ' + time.strftime("%c") + ' - ' + err_message
                        self.send_email(status)
                        #error = True
                        #break
                grids = Grid.objects.filter(scanned=False, keyword=keyword)[:numrows]
            if error:
                    break
