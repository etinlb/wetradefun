from trades.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.loader import get_template
from django.template import RequestContext
from django.template import Context
from trades import giantbomb

import datetime, random, sha
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from trades.models import UserProfile
from trades.forms import RegistrationForm

def index(request):
    return HttpResponse("Hello, world. You're at the trades index.")

def save(request, user_name):
    user=User.objects.create_user(user_name,"email","password")
    user_profile = UserProfile(user = user, address='address', rating=1)
    user_profile.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % user_profile.id)

def load(request, user_id):
    u=UserProfile.objects.get(id=user_id)
    return HttpResponse("You load a user whose name is %s." % u.user.username)

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
        gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        input=request.GET.get('q')
        message=gb.search(input)
    else:
        message="Not AJAX"
    return HttpResponse(message)

def make_offer(request):
    if request.is_ajax():
        user_id=request.GET.get('user_id')
        #user_name=UserProfile.objects.get(id=user_id).user.username
        userprofile=UserProfile.objects.get(id=user_id)
        gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        game1_id=request.GET.get('game1_id')
        game1_name=gb.getGame(int(game1_id)).name
        game2_id=request.GET.get('game2_id')
        game2_name=gb.getGame(int(game2_id)).name
        transaction=Transaction(sender=userprofile,
                sender_gianBombID=game1_id,
                receiver=userprofile,
                receiver_gianBombID=game2_id)
        transaction.save()
        # for now receiver is the same as sender
        # should write a function to support this
        transaction.save()
        message=userprofile.user.username+" take his "+game1_name+" to trade for "+game2_name
        #message=user_name+" take his "+type(game1_id).__name__+" to trade for "+game2_id
    else:
        message="Not AJAX"
    return HttpResponse(message)

def search_game(request):
    return render_to_response('search_game.html')

def sign(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = User.objects.create_user(
                form.cleaned_data['username'], 
                form.cleaned_data['email'], 
                form.cleaned_data['password'],)
            user_profile = UserProfile(user = user, address='address', rating=1)
            user_profile.save()
            return HttpResponse("You save a user. Please load his name by using id %s." % user_profile.id)
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    })
