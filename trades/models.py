from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  address = models.CharField(max_length=64)
  rating = models.IntegerField()

class Wishlist(models.Model):
  user = models.ForeignKey(UserProfile)
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

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.DateTimeField(auto_now_add=True)
  sender = models.ForeignKey(UserProfile,related_name='Message_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Message_receiver')
  transactions = models.ForeignKey(Transaction)

class Userrating (models.Model):
  rating = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Userrating_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Userrating_receiver')
