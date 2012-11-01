from django.db import models

# Create your models here.
class Trades(models.Model):
  tradesId = models.IntegerField()
  status = models.CharField(max_length=10)
  rating = models.CharField(max_length=10)
  user1Id = models.IntegerField()
  user2Id = models.IntegerField()
  game1Id = models.IntegerField()
  game2Id = models.IntegerField()