import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from user.forms import RegistrationForm
from user.models import UserProfile
from trades.models import *
import search as s

def game_details(request, game_id):
  # Is the game in wishlist?
  in_wishlist = False
  if request.user.is_authenticated():
    if Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = game_id):
      in_wishlist = True

  game = s.getGameDetsById(game_id, 'id','name', 'original_release_date', 'image', 'deck', 'genres', 'platforms', 'site_detail_url')
  try:
      num_of_listing = Currentlist.objects.filter(giantBombID = game_id).count()
  except Currentlist.DoesNotExist:
      num_of_listing = 0
  return render_to_response('game_page.html', {'game': game, 'listing': num_of_listing, 'in_wishlist': in_wishlist,})


def search(request, query):
    results = s.getList(query, 'name', 'image', 'original_release_date', 
                        'deck', 'platforms', 'id', 'genres', 'site_detail_url' )
    if results == None:
      render_to_response('no_game_found.html')
    # TODO make it get the number of listings
    for x in results:
      x['number_of_listing'] = Currentlist.objects.filter(giantBombID=x['id']).count()

      if x['number_of_listing'] == None:
        x['number_of_listing'] = 0
     
    return render_to_response('search_page.html', {'results':results})  

# TODO Handle the game page and search page buttons

# AJAX calls
def add_to_wish_list(request):  
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
  if request.is_ajax():
    try:
      Wishlist.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get('game_id')).delete()
      message=user_name+" deleted "+game_id+" from their wish list"
    except Exception, e:
      message="not in wishlist"
  else:
    message="Not AJAX" 
  return HttpResponse(message)

<<<<<<< HEAD
  def accept_offer(request):
    #TODO verify if this is correct
    if request.is_ajax():
      transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
      if transaction.status = offered
        transaction.status = accepted
        message = "Please wait for " + reciever + " to make the final trade confirmation"
      else
        message="that trade is no longer available or has already been accepted"
    else:
      message="Not AJAX"
    return HttpResponse(message)


  def decline_offer(request):
    if request.is_ajax():
      transaction = Transaction.objects.filter(transaction_id = request.GET.get('transaction_id'))
      if transaction.status = offered:
        transaction.status = declined
        message = "this listing is now closed"
    else:
      message="that trade is no longer available or has already been accepted"
    else:
      message="Not AJAX"
    return HttpResponse(message)

  def remove_listing(request):
    if request.is_ajax():
      listing = CurrentList.objects.filter(user = request.user.get_profile(), giantBombID = request.GET.get("game_id"))
      if listing.status = opened: #open is a keyword
        listing.status = closed
        message = "You have cancelled your listing"
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
    game2_id=request.GET.get('game2_id')
    if game1_id!=game2_id and len(Currentlist.objects.filter(giantBombID=game2_id))!=0:
      for currentlist in Currentlist.objects.filter(giantBombID=game2_id):
        if userprofile!=currentlist.user:
          transaction=Transaction(sender=userprofile,
                  sender_giantBombID=game1_id,
                  receiver=currentlist.user,
                  receiver_giantBombID=game2_id)
          transaction.save()
          message="Transaction saved"
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
    game_id=request.GET.get('game_id')
    currentlist=Currentlist(user=userprofile, giantBombID=game_id,)
    currentlist.save()
    message=user_name+" add "+game_id+" to his current list"
  else:
      message="Not AJAX"
  return HttpResponse(message)

