import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from user.models import UserProfile
from trades.models import *
from trades import giantbomb
import json
from django.core.exceptions import ObjectDoesNotExist
import re
import search as s

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if request.user.is_authenticated():
    # TODO make this work when game isn't found in game table, i.e add it to there
    try:
      wish_game = Game.objects.get(giant_bomb_id = game_id, platform = '' )
      if Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = wish_game):
        in_wishlist = True
    except Game.DoesNotExist:
      pass

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      num_of_listing = Currentlist.objects.filter(giantBombID = game_id).count()
  except Currentlist.DoesNotExist:
      num_of_listing = 0
  return render(request,'game_page.html', {'game': game, 'listing': num_of_listing, 'in_wishlist': in_wishlist,})


def search(request):
  if request.GET:
    query = request.GET['term']

  # Replace all runs of whitespace with a single +
  query = re.sub(r"\s+", '+', query)
  results = s.getList(query, 'name', 'image', 'original_release_date', \
    'deck', 'id', 'site_detail_url')
  if results == None:
    render_to_response('no_game_found.html')
  # TODO make it get the number of listings
  for x in results:
    x['number_of_listing'] = Currentlist.objects.filter(giantBombID=x['id']).count()

  if x['number_of_listing'] == None:
    x['number_of_listing'] = 0
  return render(request, 'search_page.html', {'results':results})

# TODO Handle the game page and search page buttons

# AJAX calls
def add_to_wish_list(request):
  # TODO make this add the foreign key
  if request.is_ajax():
    # get game from table or add if not there
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '') #CHANGE PLEASE
    # Check that is not already in wishlist
    if not Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game):
      user_id=request.GET.get('user_id')
      userprofile = request.user.get_profile()
      user_name= userprofile.user.username
      game_id=request.GET.get('game_id')
      wishlist=Wishlist(user=userprofile, wishlist_game = game)
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
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '')
    try:
      Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game).delete()
      message = user_name + " deleted " + game_id + " from their wish list"
    except Exception, e:
      message = "not in wishlist"
  else:
    message = "Not AJAX"
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
    listing = Currentlist.objects.filter(pk = request.GET.get('listing_id'))
    if (listing.count() == 1):
      listing.delete()
      message = "You have deleted your listing"
    elif (listing.count() == 0):
      message = "This listing does not exist"
    else:
      message = "ERROR: Multiple listings of this id exists"
  else:
    message="Not AJAX"
  return HttpResponse(message)

def make_offer(request):
  message = "not entered"
  if request.user.is_authenticated():
    if request.is_ajax():
      userprofile = request.user.get_profile()
      user_name = userprofile.user.username
      platform = request.GET.get('platform')
      s_game = get_game_table_by_id(request.GET.get('game1_id'), platform) # game offered
      r_game = get_game_table_by_id(request.GET.get('game2_id'), platform) # game listed
      if (s_game.giant_bomb_id != r_game.giant_bomb_id):
        message=s_game.giant_bomb_id
        for listing in Currentlist.objects.filter(game_listed = r_game):
          message="Estoy en el for"
          transaction = Transaction.objects.create(status = "offered", sender = userprofile, sender_game = s_game, receiver = listing.user, receiver_game = r_game)
          transaction.save()
          message += "\n" + str(user_name) + " offered to " + str(listing.user.user.username)
      else:
        message = "These two games are the same"
    else:
      message = "Not AJAX"
  else:
    message = "Not logged in"

  return HttpResponse(message)  

def add_listing(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()
    user_name=userprofile.user.username
    game_id = request.GET.get('game_id')
    platform = request.GET.get('platfrom')
    #game = s.getGameDetsById(game_id, 'platforms', 'image', 'name', 'id')
    game = get_game_table_by_id(game_id, platform)
    # game_id = game['id']
    #game = Game.objects.get(id=511)
    #game = add_to_game_table(game)
    currentlist = Currentlist.objects.create(user=userprofile, giantBombID=game_id, game_listed = game, status = "open")
    game.num_of_listings += 1
    currentlist.save()
    message=user_name+" add "+game_id+" to his current list"
  else:
    message="Not AJAX"
    
  return HttpResponse(message)

def get_request(request):
  if request.is_ajax():
    gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
    inputString=request.GET.get('term')
    games=gb.search(inputString)
    results=[]
    for game in games:
      game_json={}
      game_json['id']=game.id 
      game_json['value']=game.name 
      game_json['label']=game.name
      results.append(game_json)
    message=json.dumps(results)
  else:
    message="Not AJAX"
  return HttpResponse(message)


def get_platform(request, game_id):  
  if request.is_ajax(): 
    gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
    id=request.GET.get('id')
    #platforms=gb.getPlatforms(inputString)
    results = s.getGameDetsById(game_id, 'platforms')
    platforms = results['platforms']
    results = []
    id = 0
    for platform in platforms:
      platform_json={}
      platform_json['value'] = platform
      platform_json['label'] = platform
      platform_json['id'] = id
      id += 1
      results.append(platform_json)
    message=json.dumps(results)
    return HttpResponse(message) 

# def put_in_game_table(id):
def put_in_game_table(id, platform):
#>>>>>>> cb6169c106ef23a0b046c089e0b35abc5382b8fa
  # try:
  # game = Game.objects.get(giant_bomb_id = game['id'])
  # game.num_of_listings = game.num_of_listings + 1
  # game.save()
  # except ObjectDoesNotExist:
  game = s.getGameDetsById(id, 'platforms', 'image', 'name', 'id')
  game = Game(platform = platform, image_url = game['image'], \
    name =game['name'], num_of_listings = 0, giant_bomb_id = game['id'])
  game.save()
  return game

def get_game_table_by_id(id, platform):
  try:
    game = Game.objects.get(giant_bomb_id = id, platform = platform)
  except Game.DoesNotExist:
    game = put_in_game_table(id, platform)
  return game


def add_message(request):
  if request.is_ajax():
    if request.method == 'POST': # If the form has been submitted..
      transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
      userprofile = request.user.get_profile()
      usermessage = Message(content = request.POST) #??
      usermessage.save()
      if transaction.receiver == userprofile:
        transaction.receiver_message = usermessage
      elif transaction.sender == userprofile:
        transaction.receiver_message = usermessage
      message = "Your message has been successfully sent"
    else:
      message = "Error"
  else:
    message="Not AJAX"
  return HttpResponse(message)
