from django.db import models


class Place(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=250)
    place_type = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()


class Grid(models.Model):
    def __unicode__(self):
        return self.place_type + ': ' + str(self.id)

    name = models.CharField(max_length=250)
    place_type = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    scanned = models.BooleanField(default=False)
