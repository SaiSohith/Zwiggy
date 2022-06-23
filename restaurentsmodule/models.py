from django.db import models

# Create your models here.


class tablebooking(models.Model):
    name = models.CharField(max_length=100)
    tableno = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
