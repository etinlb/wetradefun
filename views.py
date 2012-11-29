from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import Http404
import search as s

def home(request):
  return render(request,'base.html')
def how_to_use(request):
	return render(request, 'staticpages/how_to_use.html')
def contact_us(request):
	return render(request, 'staticpages/contact_us.html')
def no_game_found(request):
	return render(request, 'staticpages/no_game_found.html')
