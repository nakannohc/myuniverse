from django.db import models


disaster_choice = ((1, 'Flood'),
                   (2, 'Drought'),
                   (3, 'Pest'),
                   (4, 'Fire'),
                   (5, 'Storm'),
                   (6, 'Frozen'),
                   (7, 'Hail'),
                   (0, 'Others')
                   )


class Disaster(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    disaster_type = models.IntegerField(choices=disaster_choice)
    area = models.FloatField()
