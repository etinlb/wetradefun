import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from trades.models import *
import search as s

def save(request, users_name):
    u=UserProfile(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

def game_details(request, game_id):
  game = s.getGameDetsById(game_id, 'name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      num_of_listing = Currentlist.objects.get(gameID = game_id).count()
  except Currentlist.DoesNotExist:
      num_of_listing = 0
  return render_to_response('game_page.html', {'game': game, 'listing': num_of_listing})


def search(request, query):
    results = s.getList(query, 'name', 'image', 'original_release_date', 
                        'deck', 'platforms', 'id', 'genres' )
    # TODO make it get the number of listings
    for x in results:
      x['number_of_listing'] = Currentlist.objects.filter(gameID=x['id']).count()
      if x['number_of_listing'] == None:
        x['number_of_listing'] = 0
     
    return render_to_response('search_page.html', {'results':results})  

# TODO Handle the game page and search page buttons
