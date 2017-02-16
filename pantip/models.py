from __future__ import unicode_literals
from django.db import models


class Topic(models.Model):
    def __unicode__(self):
        return self.p_tid + '::' + self.p_name

    p_tid = models.IntegerField()
    p_name = models.TextField()
    p_content = models.TextField()
    p_comments = models.TextField()


class MarkTopic(models.Model):
    def __unicode__(self):
        return '%d :: %s' % (self.p_tid, self.read)

    p_tid = models.IntegerField()
    read = models.BooleanField(default=False)
