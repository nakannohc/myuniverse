# -*- coding: utf-8 -*-
import time, smtplib, requests, json, pickle, bs4, datetime, pytz, re, xlsxwriter
from django.core.management.base import BaseCommand, CommandError
from pantip.models import MarkTopic, Topic

class Command(BaseCommand):
    help = 'Preprocess Pantip Comments'

    def handle(self, *args, **options):
        wb = xlsxwriter.Workbook('/root/pantip.xlsx')
        ws = wb.add_worksheet()
        first = 0
        last = 10
        topics = Topic.objects.all()[first:last]
        count = 0
        ws.write(0, 0, 'tid')
        ws.write(0, 1, 'year')
        ws.write(0, 2, 'title')
        ws.write(0, 3, 'content')
        ws.write(0, 4, 'comments')
        row = 1
        while topics.count() > 0:
            topics = Topic.objects.all()[first:last]
            count += topics.count()
            for topic in topics:
                topic_data = []
                topic_data.append(str(topic.p_tid))
                topic_data.append(str(topic.p_datetime.year))
                topic_name = (re.sub(' +', ' ',topic.p_name))
                topic_name = re.sub(r'^https?:\/\/.*[\r\n]*', '', topic_name, flags=re.MULTILINE)
                topic_name = re.sub(r'^http?:\/\/.*[\r\n]*', '', topic_name, flags=re.MULTILINE)
                topic_data.append(topic_name)
                content = re.sub(' +',' ',topic.p_content.replace('\n','').replace('\r',''))
                content = re.sub(r'^https?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
                content = re.sub(r'^http?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
                topic_data.append(content)
                p_comments = pickle.loads(topic.p_comments)
                for p_comment in p_comments:
                    j_comments = json.loads(p_comment)
                    # print j_comments['count']
                    comments = j_comments['comments']
                    # print comments
                    for comment in comments:
                        message = bs4.BeautifulSoup(comment['message'],'lxml')
                        message = re.sub(' +',' ', message.get_text().replace('\n','').replace('\r',''))
                        message = re.sub(r'^https?:\/\/.*[\r\n]*', '', message, flags=re.MULTILINE)
                        message = re.sub(r'^http?:\/\/.*[\r\n]*', '', message, flags=re.MULTILINE)
                        topic_data.append(message)
                ws.write(row, 0, topic_data[0])
                ws.write(row, 1, topic_data[1])
                ws.write(row, 2, topic_data[2])
                ws.write(row, 3, topic_data[3])
                all_message = u''
                for m in topic_data[4:]:
                    all_message += m
                ws.write(row, 4, all_message)
                ws.write(row, 5, topic_data[2] + topic_data[3] + all_message)
                row += 1
                # break
            first += 10
            last += 10
            # break
        wb.close()
