from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique=True)
  account = models.CharField(max_length=64)
  # password = models.CharField(max_length=64)
  # name = models.CharField(max_length=64)
  # email = models.CharField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField()
  # dateRegistered = models.IntegerField()

class Game(models.Model):
  name = models.CharField(max_length=64)
  gianBombID = models.IntegerField()
  rating = models.IntegerField()

class Wishlist(models.Model):
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Currentlist(models.Model):
  status = models.CharField(max_length=64)
  datePosted = models.IntegerField()
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField()
  dateTraded = models.IntegerField()
  senderID = models.ForeignKey(UserProfile,related_name='Transaction_senderID')
  senderGameID = models.ForeignKey(Game,related_name='Transaction_senderGameID')
  receiverID = models.ForeignKey(UserProfile,related_name='Transaction_receiverID')
  receiverGameID = models.ForeignKey(Game,related_name='Transaction_receiverGameID')

class Gamecomment(models.Model):
  content = models.CharField(max_length=64)
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  senderID = models.ForeignKey(UserProfile,related_name='Message_senderID')
  receiverID = models.ForeignKey(UserProfile,related_name='Message_receiverID')
  transactionsID = models.ForeignKey(Transaction)

class Userrating (models.Model):
  rating = models.IntegerField()
  senderID = models.ForeignKey(UserProfile,related_name='Userrating_senderID')
  receiverID = models.ForeignKey(UserProfile,related_name='Userrating_receiverID')

class Gamerating (models.Model):
  rating = models.IntegerField()
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)
