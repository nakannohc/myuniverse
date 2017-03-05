# -*- coding: utf-8 -*-
import time, smtplib, requests, json, pickle, bs4, datetime, pytz, re
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from pantip.models import MarkTopic, Topic

class Command(BaseCommand):
    help = 'Preprocess Pantip Comments'

    def handle(self, *args, **options):
        keyword = u'โกง'

        first = 0
        last = 10
        topics = Topic.objects.all()[first:last]
        count = 0

        data = []

        while topics.count() > 0:
            topics = Topic.objects.filter(p_keyword__keyword=keyword)[first:last]
            count += topics.count()
            for topic in topics:
                topic_data = list()
                topic_data.append(str(topic.p_tid))
                topic_data.append(str(topic.p_datetime.year))

                topic_name = topic.p_name
                topic_name = re.sub(r'https?:\/\/.*[\r\n]*.html?', '', topic_name, flags=re.MULTILINE)
                topic_name = re.sub(r'https?:\/\/.*[\r\n]*.\/?', '', topic_name, flags=re.MULTILINE)
                topic_name = topic_name.replace('\n','').replace('\r', '')
                topic_name = (re.sub(' +', ' ', topic_name))
                topic_data.append(topic_name)

                content = bs4.BeautifulSoup(topic.p_content, 'lxml')
                for div in content.find_all('div', {'class': 'edit-history'}):
                    div.decompose()
                content = content.get_text()
                content = re.sub(r'https?:\/\/.*[\r\n]*.html?', '', content, flags=re.MULTILINE)
                content = re.sub(r'https?:\/\/.*[\r\n]*.\/?', '', content, flags=re.MULTILINE)
                content = re.sub(' +', ' ', content)
                content = content.replace('\n', '').replace('\r', '')
                content = content.replace('[spoil]', '').replace('[/spoil]', '')
                content = content.replace(u'คลิกเพื่อดูข้อความที่ซ่อนไว้', '').replace(u'คลิกเพื่อซ่อนข้อความ', '')

                topic_data.append(content)

                p_comments = pickle.loads(topic.p_comments)
                for p_comment in p_comments:
                    j_comments = json.loads(p_comment)
                    # print j_comments['count']
                    comments = j_comments['comments']
                    # print comments
                    for comment in comments:
                        # print comment['message']
                        message = bs4.BeautifulSoup(comment['message'],'lxml')
                        for div in message.find_all('div', {'class': 'edit-history'}):
                            div.decompose()
                        message = message.get_text()
                        message = re.sub(r'https?:\/\/.*[\r\n]*.html?', '', message, flags=re.MULTILINE)
                        message = re.sub(r'https?:\/\/.*[\r\n]*.\/?', '', message, flags=re.MULTILINE)
                        message = re.sub(' +', ' ', message, flags=re.MULTILINE)
                        message = message.replace('\n', '').replace('\r', '')
                        message = message.replace('[spoil]', '').replace('[/spoil]', '')
                        message = message.replace(u'คลิกเพื่อดูข้อความที่ซ่อนไว้', '').replace(u'คลิกเพื่อซ่อนข้อความ', '')
                        topic_data.append(message)

                    all_message = u''
                    for m in topic_data[4:]:
                        all_message += unicode(m) + u' '

                    d = {'tid': topic_data[0],
                         'year': topic_data[1],
                         'title': topic_data[2],
                         'content': topic_data[3],
                         'comments': all_message,
                         'all': topic_data[2] + ' ' + topic_data[3] + ' ' + all_message}
                    data.append(d)
            first += 10
            last += 10
        df = pd.DataFrame(data, columns = ['tid', 'year', 'title', 'content', 'comments', 'all'])
        df.to_csv('pantip_' + keyword + '.csv', encoding='utf-8')
