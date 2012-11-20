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
  datePosted = models.IntegerField(default=-1)
  userID = models.ForeignKey(UserProfile)
  gameID = models.ForeignKey(Game)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField()
  dateTraded = models.IntegerField()
  senderID = models.ForeignKey(UserProfile)
  senderGameID = models.ForeignKey(Game)
  receiverID = models.ForeignKey(UserProfile)
  receiverGameID = models.ForeignKey(Game)

class Gamecomment(models.Model):
  content = models.CharField(max_length=64)
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  senderID = models.ForeignKey(UserProfile)
  receiverID = models.ForeignKey(UserProfile)
  transactionsID = models.ForeignKey(Transaction)

class Userrating (models.Model):
  rating = models.IntegerField()
  senderID = models.ForeignKey(UserProfile)
  receiverID = models.ForeignKey(UserProfile)

class Gamerating (models.Model):
  rating = models.IntegerField()
  usersID = models.ForeignKey(UserProfile)
  gamesID = models.ForeignKey(Game)
