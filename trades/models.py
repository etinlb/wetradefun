from django.contrib.auth.models import User
from django.db import models
from user.models import UserProfile

class Game(models.Model):
  name = models.CharField(max_length=64)
  gianBombID = models.IntegerField()
  rating = models.IntegerField()


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
  userID = models.ForeignKey(UserProfile)
  gameID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Gamerating (models.Model):
  rating = models.IntegerField()
  userID = models.ForeignKey(UserProfile)
  gameID = models.ForeignKey(Game)
