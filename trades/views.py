from django.contrib.auth.decorators import login_required
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
import datetime

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if request.user.is_authenticated():
    # TODO make this work when game isn't found in game table, i.e add it to there
    try:
      wish_game = Game.objects.get(giant_bomb_id = game_id, platform = '')
      if Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = wish_game):
        in_wishlist = True
    except Game.DoesNotExist:
      pass

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      platforms_listed = Game.objects.filter(giant_bomb_id = game_id).exclude(num_of_listings = 0).values_list('platform')
      platforms_count = {}
      if platforms_listed:
        for k in platforms_listed:
          v = Game.objects.get(giant_bomb_id = game_id, platform = k[0]).num_of_listings
          platforms_count[k[0]] = v
  except Currentlist.DoesNotExist:
      games_listed = 0 #why is this here?
  return render(request,'game_page.html', {'game': game, 'listings': platforms_count, 'in_wishlist': in_wishlist,})


def search(request):
  if request.GET:
    query = request.GET['term']
    offset = request.GET['offset']

  # Replace all runs of whitespace with a single +
  query = re.sub(r"\s+", '+', query)
  results = s.getList(query, offset,  'name', 'image', 'original_release_date', \
    'deck', 'id', 'site_detail_url')
  if results == None:
    return render_to_response('staticpages/no_game_found.html')
  # TODO make it get the number of listings
  for x in results:
    x['number_of_listing'] = Currentlist.objects.filter(giantBombID=x['id']).count()

  if x['number_of_listing'] == None:
    x['number_of_listing'] = 0
    
  previous=int(int(offset)-10)
  if previous == -10:
    previous=-1;
  
  next=int(int(offset)+10)
  if len(results) != 10:
    next=-1;
  
  return render(request, 'search_page.html', 
  {'results':results,
  'query':query,
  'previous':previous,
  'next':next
  })

@login_required(login_url='/users/sign_in/')
def add_to_wish_list(request):
  if request.is_ajax():
    # get game from table or add if not there
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '') #CHANGE PLEASE
    # Check that is not already in wishlist
    if (not Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game)):
      user_id = request.GET.get('user_id')
      userprofile = request.user.get_profile()
      user_name= userprofile.user.username
      game_id = request.GET.get('game_id')
      wishlist = Wishlist.objects.create(user = userprofile, wishlist_game = game)
      wishlist.save()
      message = user_name + " added " + game.name + " to their wish list"
    else:
      message = "already in wishlist"
  else:
    message = "Not AJAX"
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def remove_from_wish_list(request):
  if request.is_ajax():
    game_id = request.GET.get('game_id')
    game = get_game_table_by_id(game_id, '')
    game_in_wishlist = Wishlist.objects.filter(user = request.user.get_profile(), wishlist_game = game)
    if (game_in_wishlist.count() == 1):
      message = request.user.get_profile().user.username + " deleted " + game_in_wishlist[0].wishlist_game.name + " from their wish list"      
      game_in_wishlist[0].delete()
    else:
      message = "game not in wishlist"
  else:
    message = "Not AJAX"

  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def accept_offer(request):
  #TODO verify if this is correct
  already_accepted = False

  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    other_trans = Transaction.objects.filter(current_listing = transaction.current_listing)
    if (transaction != None):

      for ot in other_trans:
        if (ot.pk != transaction.pk and ot.status == "accepted"):
          already_accepted = True
          messages.error(request, "You have already accepted a trade offer for that listing")

      if (transaction.status == "offered" and already_accepted == False):
        transaction.status = "accepted"
        messages.success(request, "You have successfully accepted the trade offer")
        transaction.save()
      message= "Offer accepted"
    else:
      message = "No such trade exists"
  else:
    message="Not AJAX"
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def confirm_offer(request):
  #TODO verify if this is correct
  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    senders_game = transaction.sender_game
    userprofile = request.user.get_profile()
    users_other_offers = Transaction.objects.filter(sender = userprofile, sender_game = senders_game)
    if (transaction != None):
      if (transaction.status == "accepted"):
        transaction.status = "confirmed"
        transaction.dateTraded = datetime.datetime.now()
        message = "Congratulations, you have completed your transaction"
        transaction.save()

        currentlisting = Currentlist.objects.get(pk = transaction.current_listing.pk)
        # currentlisting_user = currentlisting.user
        listing_other_offers = Transaction.objects.filter(current_listing = currentlisting)
        currentlisting.status = "closed"
        game = get_game_table_by_id(currentlisting.game_listed.giant_bomb_id, currentlisting.game_listed.platform)
        game.num_of_listings -= 1
        game.save()
        currentlisting.save()

        # to delete other tranactions where the sender offered the same game too but confirmed
        for othertransactions in users_other_offers:
          if othertransactions.current_listing.game_listed == transaction.current_listing.game_listed:
            if othertransactions != transaction:
              message += "HII"
              othertransactions.delete()

        #deletes the offer from the listings
        for otheroffers in listing_other_offers:
          if otheroffers != transaction:
            message += "ASDA"
            otheroffers.delete()

      else:
        message = "This trade is no longer available or has already been confirmed"
        message = str(transaction.pk)
    else:
      message = "No such trade exists"
  else:
    message = "Not AJAX"
  messages.success(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def decline_offer(request):
  if request.is_ajax():
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    userprofile = request.user.get_profile()
    if transaction != None:
      if (transaction.status == "offered" and userprofile == transaction.current_listing.user) or (transaction.status == "accepted" and userprofile == transaction.sender):
        transaction.status = "declined"
        message = userprofile.user.username + "declined the offer"
        transaction.save()
      else:
        message="This trade is no longer available or has already been accepted"
    else:
      message = "No such trade exists"
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def delete_offer(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()    
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    if transaction != None:
      if ((userprofile == transaction.sender) and ((transaction.status == "offered") or (transaction.status == "accepted"))):
        transaction.delete()
        #message = userprofile.user.username + " deleted the offer"
      else:
        message="This trade is no longer available or has already been confirmed"
    else:
      message = "This trade does not exist"
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def remove_listing(request):
  if request.is_ajax():
    listing = Currentlist.objects.get(pk = request.GET.get('listing_id'))
    if (listing != None):
      trans = Transaction.objects.filter(current_listing = listing)
      for t in trans:
        t.delete()
      
      game_listed = listing.game_listed
      game_listed.num_of_listings -= 1
      game_listed.save()
      message = "You have deleted your listing for " + listing.game_listed.name
      listing.delete()
    else:
      message = "This listing does not exist"
  else:
    message="Not AJAX"
  messages.error(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def make_offer(request):
  message = ""
  if request.user.is_authenticated():
    if request.is_ajax():
      userprofile = request.user.get_profile()
      user_name = userprofile.user.username
      r_platform = request.GET.get('r_platform')
      s_platform = request.GET.get('s_platform')
      s_game = get_game_table_by_id(request.GET.get('game1_id'), s_platform) # sender game / game offered
      r_game = get_game_table_by_id(request.GET.get('game2_id'), r_platform) # receiver game / game listed
      if (s_game.giant_bomb_id == r_game.giant_bomb_id):
        messages.error(request, "These two games are the same games for the same platforms")
      else:
        for listing in Currentlist.objects.filter(game_listed = r_game):
          if (listing.user == userprofile):
            message = "Cannot offer a game to your own listing"
            messages.error(request,"You can't offer games to yourself. The offer you made to yourself will not be reflected")
          else:
            transaction = Transaction.objects.create(status = "offered", sender = userprofile, sender_game = s_game, current_listing = listing)
            transaction.save()

        messages.success(request, "You have made an offer for " + r_game.name + " for the " + r_game.platform)
      message = "success"
    else:
      message = "Not AJAX"
  else:
    message = "Not logged in"

  return HttpResponse(message)  

@login_required(login_url='/users/sign_in/')
def add_listing(request):
  if request.is_ajax():
    userprofile = request.user.get_profile()
    user_name = userprofile.user.username
    game_id = request.GET.get('game_id')
    platform = request.GET.get('platform')
    game = get_game_table_by_id(game_id, platform)
    currentlist = Currentlist.objects.create(user = userprofile, giantBombID = game_id, game_listed = game, status = "open")
    game.num_of_listings += 1
    game.save()
    currentlist.save()
    message  = "You have created a listing for " + game.name
  else:
    message = "Not AJAX"
  messages.success(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def rate_user(request):
  if request.is_ajax():
    message = ""
    added_rating = request.GET.get('desired_rating')
    transaction = Transaction.objects.get(pk = request.GET.get('transaction_id'))
    userprofile = request.user.get_profile()
    if (userprofile == transaction.sender or userprofile == transaction.current_listing.user):
      if (userprofile == transaction.sender):
        if (transaction.receiver_has_been_rated == None):
          userrating = transaction.current_listing.user
          transaction.receiver_has_been_rated = True
          transaction.save()
        else:
          message = "Error, You have already rated that user!"

      elif (userprofile == transaction.current_listing.user):
        if (transaction.sender_has_been_rated == None):
          userrating = transaction.sender
          transaction.sender_has_been_rated = True
          transaction.save()
        else:
          message = "Error, You have already rated that user!"

      totalRatings = userrating.num_of_ratings * userrating.rating
      userrating.num_of_ratings += 1
      totalRatings += float(added_rating)
      userrating.rating = float(totalRatings / userrating.num_of_ratings)
      message = "You have rated " + str(userrating.user.username) + " a rating of " + str(added_rating)
      userrating.save()
    else:
      message = "This trade does not exist"


  else:
    message = "Not AJAX"
  messages.success(request, message)
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

@login_required(login_url='/users/sign_in/')
def get_platform(request, game_id):  
  if request.is_ajax(): 
    gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
    id=request.GET.get('id')
    #platforms=gb.getPlatforms(inputString)
    results = s.getGameDetsById(game_id, 'platforms')
    platforms = results['platforms']
    results = []
    for platform in platforms:
      results.append(platform)
    message=json.dumps(results)
    return HttpResponse(message)

def put_in_game_table(id, platform):
  game = s.getGameDetsById(id, 'platforms', 'image', 'name', 'id')
  game = Game.objects.create(platform = platform, image_url = game['image'], \
    name = game['name'], num_of_listings = 0, giant_bomb_id = game['id'])
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
