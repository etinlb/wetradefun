from django.db import models

class User(models.Model):
  account = models.CharField(max_length=64)
  password = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField()
  dateRegistered = models.IntegerField()

class Game(models.Model):
  name = models.CharField(max_length=64)
  gianBombID = models.IntegerField()
  rating = models.IntegerField()

class Wishlist(models.Model):
  usersID = models.ForeignKey(User)
  gamesID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Currentlist(models.Model):
  status = models.CharField(max_length=64)
  datePosted = models.IntegerField()
  usersID = models.ForeignKey(User)
  gamesID = models.ForeignKey(Games)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField()
  dateTraded = models.IntegerField()
  senderID = models.ForeignKey(User)
  senderGameID = models.ForeignKey(Game)
  receiverID = models.ForeignKey(User)
  receiverGameID = models.ForeignKey(Game)

class Gamecomment(models.Model):
  content = models.CharField(max_length=64)
  usersID = models.ForeignKey(User)
  gamesID = models.ForeignKey(Game)
  datePosted = models.IntegerField()

class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField()
  senderID = models.ForeignKey(User)
  receiverID = models.ForeignKey(User)
  transactionsID = models.ForeignKey(Transactions)

class Userrating (models.Model):
  rating = models.IntegerField()
  senderID = models.ForeignKey(User)
  receiverID = models.ForeignKey(User)

class Gamerating (models.Model):
  rating = models.IntegerField()
  usersID = models.ForeignKey(User)
  gamesID = models.ForeignKey(Game)
