# from django.contrib.auth.models import User
from user.models import UserProfile
from django.db import models

class Wishlist(models.Model):
  user = models.ForeignKey(UserProfile) #, related_name='user_wishlist')
  wishlist_game = models.ForeignKey('Game') #, related_name='game_wishlist')
  datePosted = models.DateTimeField(auto_now_add=True)

class Currentlist(models.Model):
  user = models.ForeignKey(UserProfile)
  giantBombID = models.IntegerField() # DO NOT USE ANYMORE, WILL BE REMOVED SOON!!
  game_listed = models.ForeignKey('Game') # , related_name='listed_name')
  status = models.CharField(max_length=64) # OPEN/CLOSED
  datePosted = models.DateTimeField(auto_now_add=True) 

class Transaction(models.Model):
  status = models.CharField(max_length=64) # OFFERED/ACCEPTED/CONFIRMED/DEFERRED
  dateRequested = models.DateTimeField(auto_now_add=True)
  dateTraded = models.DateTimeField(null=True)
  sender = models.ForeignKey(UserProfile) # , related_name='Transaction_sender')
  sender_game = models.ForeignKey('Game') # , related_name='Transaction_sender_game')
  sender_message = models.CharField(max_length=256, null=True)
  current_listing = models.ForeignKey('Currentlist')
  sender_has_been_rated = models.NullBooleanField()
  receiver_has_been_rated = models.NullBooleanField()
  receiver_message = models.CharField(max_length=256, null=True)
  # receiver = models.ForeignKey(UserProfile, related_name='Transaction_receiver')
  # receiver_game = models.ForeignKey('Game', related_name='Transaction_receiver_game')

class Game(models.Model):
  platform = models.CharField(max_length=64)
  image_url = models.CharField(max_length=512)
  name = models.CharField(max_length=128)
  giant_bomb_id = models.IntegerField(unique=True)
  num_of_listings = models.IntegerField()

