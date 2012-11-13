from django.http import HttpResponse
from django.shortcuts import render_to_response
from trades.models import *
import search as s
from django import forms



def index(request):
    return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=Users(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

def gameDetail(request, game_id):
  game = s.getGameDetsById(game_id, 'name', 'original_release_date', 'deck', 'image')
  listing = Currentlists.objects.get(gamesID = game_id)
  if listing == None:
    listing = 'There are no listings for this game'
  return render_to_response('detail.html', {'game':game, 'listing':listing, }) #render(details.html, {'game' : game})git

from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.loader import get_template
from django.template import RequestContext
from django.template import Context
# from trades import giantbomb
from trades.forms import SearchForm


# def search_form(request):
#     return render_to_response('search_form.html')
  
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
      
    # q=request.GET.get('q')
    # response_data={}
    # response_data['q'] = q
    # response_data['message'] = 'You messed up'
    # return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

def get_json(request):
    if request.is_ajax():
        gb = giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        input=request.GET.get('q')
        message = gb.search(input)
    else:
        message = "Not AJAX"
    return HttpResponse(message)

def search_game(request):
    return render_to_response('search_game.html')