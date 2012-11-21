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
from trades.forms import *

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

def edit_offer(request, transaction_id):
    #return HttpResponse("You load a transaction whose sender_gianBombID is %s." % transaction.sender_gianBombID)
    transaction=Transaction.objects.get(id=transaction_id)
    sender_name=transaction.sender.user.username
    receiver_name=transaction.receiver.user.username
    gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
    receiver_game_name=gb.getGame(int(transaction.receiver_gianBombID)).name
    if request.method == 'POST': # If the form has been submitted...
        if 'editoffer_form_submit' in request.POST: # If registration_form is submitted
            editoffer_form = EditOfferForm(request.POST) # A form bound to the POST data
            if editoffer_form.is_valid(): # All validation rules pass
                transaction.sender_gianBombID = editoffer_form.cleaned_data['editoffer_game1_id']
                transaction.save()
                editoffer_result="success!"
                return render_to_response('edit_offer.html', {
                        'editoffer_form': editoffer_form,
                        'sender_name': sender_name,
                        'receiver_name': receiver_name,
                        'receiver_game_name': receiver_game_name,
                        'editoffer_result': editoffer_result,
                    })
    else:
        data={'editoffer_game1_id':transaction.sender_gianBombID}
        editoffer_form = EditOfferForm(data)
    return render_to_response('edit_offer.html', {
        'editoffer_form': editoffer_form,
        'sender_name': sender_name,
        'receiver_name': receiver_name,
        'receiver_game_name': receiver_game_name,
    })

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

def add_to_wish_list(request):
    if request.is_ajax():
        user_id=request.GET.get('user_id')
        userprofile=UserProfile.objects.get(id=user_id)
        user_name=userprofile.user.username
        gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        game_id=request.GET.get('game_id')
        game_name=gb.getGame(int(game_id)).name
        wishlist=Wishlist(user=userprofile,
                gianBombID=game_id,)
        wishlist.save()
        message=user_name+" add "+game_name+" to his wish list"
    else:
        message="Not AJAX"
    return HttpResponse(message)

def add_to_current_list(request):
    if request.is_ajax():
        user_id=request.GET.get('user_id')
        userprofile=UserProfile.objects.get(id=user_id)
        user_name=userprofile.user.username
        gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        game_id=request.GET.get('game_id')
        game_name=gb.getGame(int(game_id)).name
        currentlist=Currentlist(user=userprofile,
                gianBombID=game_id,)
        currentlist.save()
        message=user_name+" add "+game_name+" to his current list"
    else:
        message="Not AJAX"
    return HttpResponse(message)

def make_offer(request):
    if request.is_ajax():
        user_id=request.GET.get('user_id')
        userprofile=UserProfile.objects.get(id=user_id)
        user_name=userprofile.user.username
        gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
        game1_id=request.GET.get('game1_id')
        game1_name=gb.getGame(int(game1_id)).name
        game2_id=request.GET.get('game2_id')
        game2_name=gb.getGame(int(game2_id)).name
        if game1_id!=game2_id and len(Currentlist.objects.filter(gianBombID=game2_id))!=0:
            message=user_name+" want to take his "+game1_name+" to trade for "+game2_name+" owned by "
            for currentlist in Currentlist.objects.filter(gianBombID=game2_id):
                #if userprofile!=currentlist.user and game1_id!=game2_id:
                if userprofile!=currentlist.user:
                    message+=currentlist.user.user.username+", "
                    transaction=Transaction(sender=userprofile,
                            sender_gianBombID=game1_id,
                            receiver=currentlist.user,
                            receiver_gianBombID=game2_id)
                    transaction.save()
            message+="... "
        elif game1_id==game2_id:
            message="These two games are the same"
        elif len(Currentlist.objects.filter(gianBombID=game2_id))==0:
            message="No one has target game "+game2_name
    else:
        message="Not AJAX"
    return HttpResponse(message)

def search_game(request):
    return render_to_response('search_game.html')

def sign(request):
    if request.method == 'POST': # If the form has been submitted...
        if 'registration_form_submit' in request.POST: # If registration_form is submitted
            registration_form = RegistrationForm(request.POST) # A form bound to the POST data
            makeoffer_form = MakeOfferForm() # An unbound form
            makeofferajax_form = MakeOfferAjaxForm() # An unbound form
            if registration_form.is_valid(): # All validation rules pass
                # Process the data in registration_form.cleaned_data
                user = User.objects.create_user(
                    registration_form.cleaned_data['username'], 
                    registration_form.cleaned_data['email'], 
                    registration_form.cleaned_data['password'],)
                user_profile = UserProfile(user = user, address='address', rating=1)
                user_profile.save()
                result="You save a user. Please load his name by using id %s." % user_profile.id
                return render_to_response('users/sign.html', {
                    'registration_form': registration_form,
                    'makeoffer_form': makeoffer_form,
                    'makeofferajax_form': makeofferajax_form,
                    'registration_result': result,
                    'registration_userID': user_profile.id,
                })
        elif 'makeoffer_form_submit' in request.POST: # If makeoffer_form is submitted
            registration_form = RegistrationForm() # An unbound form
            makeoffer_form = MakeOfferForm(request.POST) # A form bound to the POST data
            makeofferajax_form = MakeOfferAjaxForm() # An unbound form
            if makeoffer_form.is_valid(): # All validation rules pass
                # Process the data in makeoffer_form.cleaned_data
                user_id=makeoffer_form.cleaned_data['makeoffer_user_id']
                userprofile=UserProfile.objects.get(id=user_id)
                user_name=userprofile.user.username
                gb=giantbomb.Api('c815f273a0003ab1adf7284a4b2d61ce16d3d610')
                game1_id=makeoffer_form.cleaned_data['makeoffer_game1_id']
                game1_name=gb.getGame(int(game1_id)).name
                game2_id=makeoffer_form.cleaned_data['makeoffer_game2_id']
                game2_name=gb.getGame(int(game2_id)).name
                if game1_id!=game2_id:
                    result=user_name+" want to take his "+game1_name+" to trade for "+game2_name+" owned by "
                    for currentlist in Currentlist.objects.filter(gianBombID=game2_id):
                        #if userprofile!=currentlist.user and game1_id!=game2_id:
                        if userprofile!=currentlist.user:
                            result+=currentlist.user.user.username+", "
                            transaction=Transaction(sender=userprofile,
                                    sender_gianBombID=game1_id,
                                    receiver=currentlist.user,
                                    receiver_gianBombID=game2_id)
                            transaction.save()
                    result+="... "
                    return render_to_response('users/sign.html', {
                        'registration_form': registration_form,
                        'makeoffer_form': makeoffer_form,
                        'makeofferajax_form': makeofferajax_form,
                        'makeoffer_result': result,
			    		'editofferID': transaction.id,
                })
                else:
                    result="These two games are the same"
                return render_to_response('users/sign.html', {
                    'registration_form': registration_form,
                    'makeoffer_form': makeoffer_form,
                    'makeofferajax_form': makeofferajax_form,
                    'makeoffer_result': result,
                })
        else: # To avoid unbound error
            registration_form = RegistrationForm() # An unbound form
            makeoffer_form = MakeOfferForm() # An unbound form
            makeofferajax_form = MakeOfferAjaxForm() # An unbound form
    else: # First attempt to the webpage
        registration_form = RegistrationForm() # An unbound form
        makeoffer_form = MakeOfferForm() # An unbound form
        makeofferajax_form = MakeOfferAjaxForm() # An unbound form

    return render_to_response('users/sign.html', {
        'registration_form': registration_form,
        'makeoffer_form': makeoffer_form,
        'makeofferajax_form': makeofferajax_form,
    })
