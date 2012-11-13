from django.db import models

class Users(models.Model):
  account = models.CharField(max_length=64)
  password = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField(default=-1)
  dateRegistered = models.IntegerField(default=-1)

class Games(models.Model):
  name = models.CharField(max_length=64)
  gianBombID = models.IntegerField(default=-1)
  rating = models.IntegerField(default=-1)

class Wishlists(models.Model):
  usersID = models.ForeignKey(Users)
  gamesID = models.ForeignKey(Games)
  datePosted = models.IntegerField(default=-1)

class Currentlists(models.Model):
  status = models.CharField(max_length=64)
  datePosted = models.IntegerField(default=-1)
  usersID = models.ForeignKey(Users)
  gamesID = models.ForeignKey(Games)

class Transactions(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField(default=-1)
  dateTraded = models.IntegerField(default=-1)
  senderID = models.ForeignKey(Users)
  senderGameID = models.ForeignKey(Games)
  receiverID = models.ForeignKey(Users)
  receiverGameID = models.ForeignKey(Games)

class Gamecomments (models.Model):
  content = models.CharField(max_length=64)
  usersID = models.ForeignKey(Users)
  gamesID = models.ForeignKey(Games)
  datePosted = models.IntegerField(default=-1)

class Messages (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField(default=-1)
  senderID = models.ForeignKey(Users)
  receiverID = models.ForeignKey(Users)
  transactionsID = models.ForeignKey(Transactions)

class Userratings (models.Model):
  rating = models.IntegerField(default=-1)
  senderID = models.ForeignKey(Users)
  receiverID = models.ForeignKey(Users)

class Gameratings (models.Model):
  rating = models.IntegerField(default=-1)
  usersID = models.ForeignKey(Users)
  gamesID = models.ForeignKey(Games)
