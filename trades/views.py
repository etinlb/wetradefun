import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from user.models import UserProfile
from trades.models import *
from django.core.exceptions import ObjectDoesNotExist
import re
import search as s

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if request.user.is_authenticated():
    # TODO make this work when game isn't found in game table, i.e add it to there
    game = Game.objects.get(giant_bomb_id = game_id )
    if Wishlist.objects.filter(user = request.user.get_profile(), game_wanted = game):
      in_wishlist = True

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      num_of_listing = Currentlist.objects.filter(giantBombID = game_id).count()
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
  # TODO make this add the foreign key 
  if request.is_ajax():
    # Check that is not already in wishlist
    if not Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get('game_id')):    
      user_id=request.GET.get('user_id')
      userprofile = request.user.get_profile()
      user_name= userprofile.user.username
      game_id=request.GET.get('game_id')
      wishlist=Wishlist(user=userprofile, giantBombID=game_id,)
      wishlist.save()
      message=user_name+" added "+game_id+" to their wish list"
    else:
      message="already in wishlist"
  else:
    message="Not AJAX" 
  return HttpResponse(message)

def remove_from_wish_list(request): 
  # TODO make this work with the foreign key 
  if request.is_ajax():
    try:
      Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get('game_id')).delete()
      message=user_name+" deleted "+game_id+" from their wish list"
    except Exception, e:
      message="not in wishlist"
  else:
    message="Not AJAX" 
  return HttpResponse(message)

def accept_offer(request):
  #TODO verify if this is correct
  if request.is_ajax():
    transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
    if transaction.status == "offered":
      transaction.status = "accepted"
      message = "Please wait for " + reciever + " to make the final trade confirmation"
      transaction.save()
    else:
      message="that trade is no longer available or has already been accepted"
  else:
    message="Not AJAX"
  return HttpResponse(message)


def decline_offer(request):
  if request.is_ajax():
    transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
    if transaction.status == "offered":
      transaction.status = "declined"
      message = "this listing is now closed"
      transaction.save()
    else:
      message="that trade is no longer available or has already been accepted"
  else:
    message="Not AJAX"
  return HttpResponse(message)

def remove_listing(request):
  # TODO make this with the foreign key game
  if request.is_ajax():
    listing = CurrentList.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get("game_id"))
    if listing.status == "opened": #open is a keyword
      listing.status = "closed"
      message = "You have cancelled your listing"
      listing.save()
    else:
      message="You have already cancelled this listing or the trade has been finalized."
  else:
    message="Not AJAX"
  return HttpResponse(message)


def make_offer(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()
    user_name=userprofile.user.username
    game1_id=request.GET.get('game1_id')
    game1 = s.getGameDetsById(game1_id, 'platforms', 'image', 'name', 'id')
    game1 = get_game_table(game1)
    game2_id=request.GET.get('game2_id')
    game2 = s.getGameDetsById(game2_id, 'platforms', 'image', 'name', 'id')
    game2 = get_game_table(game2)
    if game1_id!=game2_id and len(Currentlist.objects.filter(giantBombID=game2_id))!=0:
      for currentlist in Currentlist.objects.filter(giantBombID=game2_id):
        if userprofile!=currentlist.user:
          transaction=Transaction(sender=userprofile,
                  sender_game=game1,
                  receiver=currentlist.user,
                  receiver_game=game2,
                  status = 'pending')
          transaction.save()
          message="Transaction saved"
        else:
          message="You already have that game" #we should try to convey these to the user better
    elif game1_id==game2_id:
      message="These two games are the same"
    elif len(Currentlist.objects.filter(giantBombID=game2_id))==0:
      message="No one has that game"
  else:
    message="Not AJAX"
  return HttpResponse(message)

def add_to_current_list(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()
    user_name=userprofile.user.username
    game_id = request.GET.get('game_id')
    game = s.getGameDetsById(game_id, 'platforms', 'image', 'name', 'id')
    game = get_game_table(game)
    # game_id = game['id']
    #game = Game.objects.get(id=511)
    #game = add_to_game_table(game)
    currentlist=Currentlist(user=userprofile, giantBombID=game_id, game_listed = game)
    currentlist.save()
    message=user_name+" add "+game_id+" to his current list"
  else:
      message="Not AJAX"
  return HttpResponse(message)

def get_game_table(game):
  try:
    game = Game.objects.get(giant_bomb_id = game['id'])
    game.num_of_listings = game.num_of_listings + 1
    game.save()
  except ObjectDoesNotExist:
    game = Game(platform = game['platforms'], image_url = game['image'], \
      name =game['name'], num_of_listings = 1, giant_bomb_id = game['id'])
    game.save()
  return game  

