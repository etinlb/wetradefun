import datetime, random, sha

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from trades.forms import RegistrationForm

from trades.models import *
import search as s
from trades.forms import SearchForm

def sign_up(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = User.objects.create_user(
                form.cleaned_data['username'], 
                form.cleaned_data['email'], 
                form.cleaned_data['password'],)
            user_profile = UserProfile(user = user, account='account', address='address', rating=1)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for registering %s' % user.username)
            # Login the user
            login(request, user)
            # Send to home page

        else:
            messages.add_message(request, messages.ERROR, form._errors['__all__'])
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))

# def index(request):
#     return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=UserProfile(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

def gamepage(request):
  gameDict = {'genres': 'awesome', 'name': 'Ratchet & Clank: Up Your Arsenal', \
  'deck': 'Ratchet & Clank:  Up Your Arsenal is the third game in the Ratchet \
  and Clank series. It is also the first to include online play.', \
  'image': 'http://media.giantbomb.com/uploads/8/87209/1974402-box_racuya_super.png', \
  'original_release_date': '2004-11-03', 'id': '4966', 'platforms': 'PS3'}
  currentNumOfListing = '1000'
  #note platfrom may be a list
  return render_to_response('gamePage.html', {'game':gameDict, 'numberOfListing':currentNumOfListing})

def gameDetail(request, game_id):
  game = s.getGameDetsById(game_id, 'name', 'original_release_date', 'deck', 'image')
  listing = Currentlists.objects.get(gamesID = game_id)
  if listing == None:
    listing = 'There are no listings for this game'
  return render_to_response('detail.html', {'game':game, 'listing':listing, }) #render(details.html, {'game' : game})git


def search(request):
    results = 'j'
    if request.method == 'POST': #form
        form = SearchForm(request.POST)
        # test = request.POST['q']
        if form.is_valid():
            query = form.cleaned_data['query']
            results = s.getList(query, 'name', 'image' )
            # test = 'true'
    else:
        form  = SearchForm()
    return render_to_response('Search.html', {'form': form, 't':results})  

