# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class TopicKeyword(models.Model):
    def __unicode__(self):
        return '%s' % (self.keyword)
    
    keyword = models.CharField(max_length=255)


class Topic(models.Model):
    def __unicode__(self):
        return '%d :: %s' % (self.p_tid, self.p_name)

    p_tid = models.IntegerField()
    p_name = models.TextField()
    p_content = models.TextField()
    p_comments = models.TextField()
    p_datetime = models.DateTimeField()
    p_keyword = models.ForeignKey('pantip.TopicKeyword', null=True, on_delete=models.CASCADE)

class MarkTopic(models.Model):
    def __unicode__(self):
        return '%d :: %s' % (self.p_tid, self.read)

    p_tid = models.IntegerField()
    p_keyword = models.ForeignKey('pantip.TopicKeyword', null=True, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

