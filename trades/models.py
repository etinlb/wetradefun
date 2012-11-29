# from django.contrib.auth.models import User
from user.models import UserProfile
from django.db import models

# class UserProfile(models.Model):
#   user = models.ForeignKey(User, unique=True)
#   address = models.CharField(max_length=64)
#   rating = models.IntegerField()

class Wishlist(models.Model):
  user = models.ForeignKey(UserProfile, related_name='user_wishlist')
  game_wanted = models.ForeignKey('Game')
  datePosted = models.DateTimeField(auto_now_add=True)

class Currentlist(models.Model):
  user = models.ForeignKey(UserProfile)
  giantBombID = models.IntegerField()
  game_listed = models.ForeignKey('Game', related_name='listed_name')
  status = models.CharField(max_length=64)
  datePosted = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
  status = models.CharField(max_length=64)
  dateRequested = models.DateTimeField(auto_now_add=True)
  dateTraded = models.CharField(max_length=64)
  sender = models.ForeignKey(UserProfile,related_name='Transaction_sender')
  sender_game = models.ForeignKey('Game',  related_name='Transaction_sender_game')
  receiver = models.ForeignKey(UserProfile,related_name='Transaction_receiver')
  receiver_game = models.ForeignKey('Game', related_name='Transaction_receiver_game')

class Game(models.Model):
  platform = models.CharField(max_length=64)
  image_url = models.CharField(max_length=500)
  name = models.CharField(max_length=100)
  giant_bomb_id = models.IntegerField(unique=True)
  num_of_listings = models.IntegerField()
  #deck = models.CharField(max_length=256)


