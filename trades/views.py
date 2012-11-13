from trades.models import User, Game
from trades.models import Wishlist, Currentlist, Transaction
from trades.models import Gamecomment, Message, Userrating, Gamerating
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.loader import get_template
from django.template import RequestContext
from django.template import Context
from trades import giantbomb

def index(request):
    return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=User(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=User.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

def search_form(request):
    return render_to_response('search_form.html')
	
def post_request(request):
    account=request.POST.get('account')
    password=request.POST.get('password')
    email=request.POST.get('email')
    response_data={}
    response_data['account'] = account
    response_data['password'] = password
    response_data['email'] = email
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

def get_request(request):
    if request.is_ajax():
        gb = giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        input=request.GET.get('q')
        message = gb.search(input)
    else:
        message = "Not AJAX"
    return HttpResponse(message)

def search_game(request):
    return render_to_response('search_game.html')
