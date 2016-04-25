from django.db import models


class Grid(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=250)
    place_type = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()
    scanned = models.BooleanField(default=False)


class Place(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=250)
    place_type = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.TextField()
    grid = models.ForeignKey(Grid, blank=True, null=True)

