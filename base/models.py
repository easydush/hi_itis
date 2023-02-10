from django.db import models


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=40)
    course = models.PositiveSmallIntegerField()
