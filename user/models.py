from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True, null=True)
  address = models.CharField(max_length=64, null=True)
  rating = models.FloatField(null=True) #NEEDS TO HAVE NULL=True
  num_of_ratings = models.IntegerField(null=True)
  #rating = models.IntegerField()
  #num_of_ratings = models.IntegerField()
