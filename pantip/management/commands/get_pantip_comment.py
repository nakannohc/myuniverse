# -*- coding: utf-8 -*-
import time, smtplib, requests, json, pickle, bs4, datetime, pytz
from django.core.management.base import BaseCommand, CommandError
from pantip.models import MarkTopic, Topic

class Command(BaseCommand):
    help = 'Get Comment From Topic'

    def send_email(self, message):
        gmail_user = 'nakannohc@gmail.com'
        gmail_pwd = 'qTut0L2$'
        FROM = 'nakannohc@gmail.com'
        TO = 'chonnakan.r@gmail.com'
        SUBJECT = 'Message from Pantip Project %s' % time.strftime("%c")
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
        url = 'https://pantip.com/forum/topic/render_comments/'
        limit_row = 5
        # self.send_email("start get topic content")

        unreads = MarkTopic.objects.filter(read=False)[0:limit_row]
        while len(unreads) > 0:
            unreads = MarkTopic.objects.filter(read=False)[0:limit_row]

            for unread in unreads:
                print unread.p_tid
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0"}
                r = requests.get('https://pantip.com/topic/' + str(unread.p_tid))
                print r.status_code
                while r.status_code != 200:
                    time.sleep(2)
                    r = requests.get('https://pantip.com/topic/' + str(unread.p_tid))
                    print r.status_code
                s = bs4.BeautifulSoup(r.content, "lxml")
                # print s
                topic = s.find('h2', {'class': 'display-post-title'})
                topic = topic.get_text()
                content = s.find('div', {'class': 'display-post-story'})
                content = content.get_text()
                dt = s.find('abbr', {'class': 'timeago'})
                d = dt['data-utime'].split(' ')[0]
                t = dt['data-utime'].split(' ')[1]
                dt = datetime.datetime(int(d.split('/')[2]),
                                       int(d.split('/')[0]),
                                       int(d.split('/')[1]),
                                       int(t.split(':')[0]),
                                       int(t.split(':')[1]),
                                       int(t.split(':')[2]),
                                       tzinfo=pytz.utc
                                       )
                total_comments = 0
                count_comment = -1
                page = 1
                comments = []
                headers["X-Requested-With"] = "XMLHttpRequest"
                params = {"tid": unread.p_tid,
                          "param": "page1",
                          "type": "1",
                          "page": "1",
                          "_": str(int(time.time()))
                          }
                while count_comment < total_comments:
                    if count_comment == -1:
                        count_comment = 0
                    params["param"] = "page" + str(page)
                    params["page"] = str(page)
                    r = requests.get(url, params=params, headers=headers)
                    # print r.url
                    data = json.loads(r.text)
                    # print data
                    # print json.dumps(data)
                    if 'count' in data:
                        total_comments = data['count']
                        count_comment += len(data['comments'])
                        comments.append(json.dumps(data))
                        page += 1
                    else:
                        break
                    time.sleep(2)
                # print comments
                p = pickle.dumps(comments)
                tp = Topic(p_tid=unread.p_tid,
                          p_name=topic,
                          p_content=content,
                          p_comments=p,
                          p_datetime=dt)
                tp.save()
                unread.read = True
                unread.save()
