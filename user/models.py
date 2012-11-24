from django.contrib.auth.models import User
from django.db import models
# from trades.models import Transaction 

# Create your models here.
class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True, null=True)
  #account = models.CharField(max_length=64)
  # password = models.CharField(max_length=64)
  # name = models.CharField(max_length=64)
  # email = models.CharField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField()
  # dateRegistered = models.IntegerField()

class Wishlist(models.Model):
  userID = models.ForeignKey(UserProfile)
  #gameID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  senderID = models.ForeignKey(UserProfile)
  receiverID = models.ForeignKey(UserProfile)
  transactionID = models.ForeignKey('trades.models', verbose_name=u'Transaction')

class Userrating (models.Model):
  rating = models.IntegerField()
  senderID = models.ForeignKey(UserProfile)
  receiverID = models.ForeignKey(UserProfile)