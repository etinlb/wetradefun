from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  address = models.CharField(max_length=64)
  rating = models.IntegerField()

class Wishlist(models.Model):
  user = models.ForeignKey(UserProfile)
  gianBombID = models.IntegerField()
  datePosted = models.IntegerField()

class Currentlist(models.Model):
  user = models.ForeignKey(UserProfile)
  gianBombID = models.IntegerField()
  status = models.CharField(max_length=64)
  datePosted = models.IntegerField()

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField()
  dateTraded = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Transaction_sender')
  sender_gianBombID = models.IntegerField()
  receiver = models.ForeignKey(UserProfile,related_name='Transaction_receiver')
  receiver_gianBombID = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Message_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Message_receiver')
  transactions = models.ForeignKey(Transaction)

class Userrating (models.Model):
  rating = models.IntegerField()
  sender = models.ForeignKey(UserProfile,related_name='Userrating_sender')
  receiver = models.ForeignKey(UserProfile,related_name='Userrating_receiver')
