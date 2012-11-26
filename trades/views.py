import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from user.models import UserProfile
from trades.models import *
import re
import search as s

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = game_id):
    in_wishlist = True

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      num_of_listing = Currentlist.objects.get(giantBombID = game_id).count()
  except Currentlist.DoesNotExist:
      num_of_listing = 0
  return render(request,'game_page.html', {'game': game, 'listing': num_of_listing, 'in_wishlist': in_wishlist,})


def search(request):
  if request.GET:
    query = request.GET['term']

  # Replace all runs of whitespace with a single dash
  query = re.sub(r"\s+", '+', query)

  results = s.getList(query, 'name', 'image', 'original_release_date', 
                      'deck', 'platforms', 'id', 'genres', 'site_detail_url' )
  if results == None:
    render_to_response('no_game_found.html')
  # TODO make it get the number of listings
  for x in results:
    x['number_of_listing'] = Currentlist.objects.filter(giantBombID=x['id']).count()

    if x['number_of_listing'] == None:
      x['number_of_listing'] = 0
   
  return render(request,'search_page.html', {'results':results})  

# TODO Handle the game page and search page buttons

# AJAX calls
def add_to_wish_list(request):  
  if request.is_ajax():
    # Check that is not already in wishlist
    if not Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get('game_id')):    
      user_id=request.GET.get('user_id')
      userprofile = request.user.get_profile()
      user_name=userprofile.user.username
      game_id=request.GET.get('game_id')
      wishlist=Wishlist(user=userprofile, giantBombID=game_id,)
      wishlist.save()
      message=user_name+" add "+game_id+" to his wish list"
    else:
      message="already in wishlist"
  else:
    message="Not AJAX" 
  return HttpResponse(message)

# AJAX calls
def remove_from_wish_list(request):  
  if request.is_ajax():
    try:
      Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get('game_id')).delete()
      message=user_name+" delete "+game_id+" from his wish list"
    except Exception, e:
      message="not in wishlist"
  else:
    message="Not AJAX" 
  return HttpResponse(message)
