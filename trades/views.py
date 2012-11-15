from django.http import HttpResponse
from django.shortcuts import render_to_response
from trades.models import *
import search as s
from trades.forms import SearchForm


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
    return render_to_response('Search.html', {'form': form, 't':results})  # Create your views here.
