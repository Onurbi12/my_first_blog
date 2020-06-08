from django.db import models


class data(models.Model):
    nbr_click =  models.IntegerField()
    link =models.CharField(max_length=30)
