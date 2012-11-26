# from django.contrib.auth.models import User
from user.models import UserProfile
from django.db import models

# class UserProfile(models.Model):
#   user = models.ForeignKey(User, unique=True)
#   address = models.CharField(max_length=64)
#   rating = models.IntegerField()

class Wishlist(models.Model):
  user = models.ForeignKey(UserProfile, related_name='user_wishlist')
  giantBombID = models.IntegerField()
  datePosted = models.DateTimeField(auto_now_add=True)

class Currentlist(models.Model):
  user = models.ForeignKey(UserProfile)
  giantBombID = models.IntegerField()
  status = models.CharField(max_length=64)
  datePosted = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.DateTimeField(auto_now_add=True)
  dateTraded = models.CharField(max_length=64)
  sender = models.ForeignKey(UserProfile,related_name='Transaction_sender')
  sender_giantBombID = models.IntegerField()
  receiver = models.ForeignKey(UserProfile,related_name='Transaction_receiver')
  receiver_giantBombID = models.IntegerField()


