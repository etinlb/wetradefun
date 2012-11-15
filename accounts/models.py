from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
  account = models.CharField(max_length=64)
  password = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  email = models.EmailField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField(default=-1)
  dateRegistered = models.IntegerField(default=-1)