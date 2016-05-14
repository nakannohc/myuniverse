# -*- coding: utf-8 -*-
import time
import smtplib
import json
import math
from difflib import SequenceMatcher
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
        error = False
        error_r = 0.001
        #self.send_email('Start Repair Places - %s' % time.strftime("%c"))
        while places.count() and not error > 0:
            for place in places:
                #print g.keyword,
                pp, status, err_message = nearby_search(str(place.lat), str(place.lng), '1', place.name)
                #print status
                print pp
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
                    #print len(pp)
                    maprob = 0.0
                    mnprob = 0.0
                    dest = None
                    print len(pp)
                    for p in pp:
                        #print '%d --- %s, %f - %s %f' % (place.id, p['name'], p['geometry']['location']['lat'], place.name, place.lat),
                        #print p['name'] == place.name,
                        #print p['geometry']['location']['lat'] - place.lat
                        #print p['geometry']['location']['lng'] - place.lng
                        #print p
                        #if p['formatted_address'] == place.address:
                        #aprob = SequenceMatcher(None,p['formatted_address'], place.address).ratio()
                        nprob = SequenceMatcher(None, p['name'], place.name).ratio()

                        print '%s --- %s = %f' % (place.name, p['name'], nprob)
                        #if aprob > maprob and aprob > 0.7:
                        #    maprob = aprob
                        #   dest = p

                        if nprob > mnprob and nprob > 0.7:
                            mnprob = nprob
                            dest = p
                    print '*'*100
                    if dest is not None:
                        #print '%s - %s' % (dest['name'], place.name)
                        place_detail, status, err_message = get_detail(dest['place_id'])
                        #print place_detail
                        if 'permanently_closed' in place_detail:
                            place.permanently_closed = True
                        else:
                            place.permanently_closed = False
                        place.place_id = place_detail['place_id']
                        place.place_detail = json.dumps(place_detail)
                        place.save()
                    else:
                        #print '%s - %s' % (dest['name'], place.name)
                        place.place_id = '####'
                        place.place_detail = '####'
                        place.save()
                else:
                    print status + ' - ' + time.strftime("%c") + ' - ' + err_message
                    self.send_email(status)
                    error = True
                    break
            places = Place.objects.filter(place_id=None)[:numrows]

