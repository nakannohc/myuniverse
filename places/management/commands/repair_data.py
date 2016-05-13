# -*- coding: utf-8 -*-
import time
import smtplib
import json
from django.core.management.base import BaseCommand, CommandError
from places.models import Place, Grid, KeywordSummary
from places.views import get_detail, radar_search, text_search, nearby_search


class Command(BaseCommand):
    help = 'Repair places'

    def send_email(self, message):
        gmail_user = 'nakannohc@gmail.com'
        gmail_pwd = 'qTut0L2$'
        FROM = 'nakannohc@gmail.com'
        TO = 'chonnakan.r@gmail.com'
        SUBJECT = 'Message from server %s' % time.strftime("%c")
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
        numrows = 10
        places = Place.objects.filter(place_id=None)[:numrows]
        print len(places)
        count_api = 0
        error = False
        #self.send_email('Start Repair Places - %s' % time.strftime("%c"))
        while places.count() and not error > 0:
            for place in places:
                #print g.keyword,
                pp, status, err_message = nearby_search(str(place.lat), str(place.lng), '1', place.name)
                #print status
                if status == 'OVER_QUERY_LIMIT':
                    print '%s - OVER_QUERY_LIMIT - %s' % (time.strftime("%c"), err_message)
                    self.send_email('OVER_QUERY_LIMIT')
                    error = True
                    break
                elif status == 'REQUEST_DENIED':
                    print '%s - REQUEST_DENIED - %s' % (time.strftime("%c"), err_message)
                    self.send_email('REQUEST_DENIED')
                    error = True
                    break
                elif status == 'INVALID_REQUEST':
                    print '%s - INVALID_REQUEST- %s' % (time.strftime("%c"), err_message)
                    self.send_email('INVALID_REQUEST')
                    error = True
                    break
                elif status == 'ZERO_RESULTS':
                    #print '%s - ZERO' % time.strftime("%c")
                    places = []
                elif status == 'OK':
                    for p in pp:
                        if p['name'] == place.name:
                            place_detail, status, err_message = get_detail(p['place_id'])
                            print place_detail
                            if 'permanently_closed' in place_detail:
                                place.permanently_closed = True
                            else:
                                place.permanently_closed = False
                            place.place_id = place_detail['place_id']
                            place.place_detail = json.dumps(place_detail)
                            place.save()
                        else:
                            print '*'*100
                else:
                    print status + ' - ' + time.strftime("%c") + ' - ' + err_message
                    self.send_email(status)
                    error = True
                    break
            break
            places = Place.objects.filter(place_id='')[:numrows]

