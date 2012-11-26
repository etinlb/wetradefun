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
  address = models.CharField(max_length=64, null=True)
  rating = models.IntegerField(null=True)
  # dateRegistered = models.IntegerField()

class Wishlist(models.Model):
  userID = models.ForeignKey(UserProfile)
  #gameID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Message_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Message_receiver')
  transaction = models.ForeignKey('trades.Transaction')#, verbose_name=u'Transaction')

# class Userrating (models.Model):
#   rating = models.IntegerField()
#   senderID = models.ForeignKey(UserProfile)
#   receiverID = models.ForeignKey(UserProfile)

# class Message (models.Model):
#   content = models.CharField(max_length=128)
#   datePosted = models.DateTimeField(auto_now_add=True)
#   sender = models.ForeignKey(UserProfile,)
#   receiver = models.ForeignKey(UserProfile,related_name='Message_receiver')
#   transactions = models.ForeignKey(Transaction)

class Userrating (models.Model):
  rating = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Userrating_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Userrating_receiver')