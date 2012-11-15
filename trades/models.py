from django.db import models

class User(models.Model):
  account = models.CharField(max_length=64)
  password = models.CharField(max_length=64)
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  address = models.CharField(max_length=64)
  rating = models.IntegerField(default=-1)
  dateRegistered = models.IntegerField(default=-1)

class Game(models.Model):
  name = models.CharField(max_length=64)
  gianBombID = models.IntegerField(default=-1)
  rating = models.IntegerField(default=-1)

class Wishlist(models.Model):
  userID = models.ForeignKey(User)
  gameID = models.ForeignKey(Game)
  datePosted = models.IntegerField(default=-1)

class Currentlist(models.Model):
  status = models.CharField(max_length=64)
  datePosted = models.IntegerField(default=-1)
  userID = models.ForeignKey(User)
  gameID = models.ForeignKey(Game)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.IntegerField(default=-1)
  dateTraded = models.IntegerField(default=-1)
  senderID = models.ForeignKey(User)
  senderGameID = models.ForeignKey(Game)
  receiverID = models.ForeignKey(User)
  receiverGameID = models.ForeignKey(Game)

class Gamecomment(models.Model):
  content = models.CharField(max_length=64)
  userID = models.ForeignKey(User)
  gameID = models.ForeignKey(Game)
  datePosted = models.IntegerField(default=-1)


class Message (models.Model):
  content = models.CharField(max_length=128)
  datePosted = models.IntegerField(default=-1)
  senderID = models.ForeignKey(User)
  receiverID = models.ForeignKey(User)
  transactionID = models.ForeignKey(Transaction)

class Userratings (models.Model):
  rating = models.IntegerField(default=-1)
  senderID = models.ForeignKey(User)
  receiverID = models.ForeignKey(User)

class Gameratings (models.Model):
  rating = models.IntegerField(default=-1)
  userID = models.ForeignKey(User)
  gameID = models.ForeignKey(Game)

