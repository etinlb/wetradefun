from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from user.forms import RegistrationForm, LoginForm
from user import sort

from trades.models import *

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q

import search as s
# from trades.forms import SearchForm

@login_required(login_url='/users/sign_in/')
def sign_out(request):
  logout(request)
  return HttpResponseRedirect('/users/sign_in')

def sign_in(request):
  # If it's 
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  else:
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                  login(request, user)
                  # Redirect to a success page.
                  messages.add_message(request, messages.SUCCESS, 'Welcome %s!' % user.username)
                  return HttpResponseRedirect('/')
                else:
                  # Return a 'disabled account' error message
                  messages.add_message(request, messages.ERROR, 'Your account is disabled')
            else:
              # Return an 'invalid login' error message.
              messages.add_message(request, messages.ERROR, 'Your username or password is incorrect')
    else:
        form = LoginForm() # An unbound form

  return render_to_response('users/sign_in.html', {
      'form': form,
  },
   context_instance=RequestContext(request))

@login_required(login_url='/users/sign_in/')
def account_management(request):
  listing_list = {}
  listing_dict = {}
  userprofiler = request.user.get_profile()
  current_listings = list(Currentlist.objects.filter(user = request.user.get_profile(), status = 'open').order_by('-datePosted'))
  for idx, listing in enumerate(current_listings):
    listing_dict[listing] = list(Transaction.objects.filter(status = 'offered', current_listing = listing))

  #assert false
  current_offers = list(Transaction.objects.filter(status = 'offered', sender = request.user.get_profile()))   
  current_offers_accepted = list(Transaction.objects.filter(status = 'accepted', sender = request.user.get_profile()))
  current_offers.extend(current_offers_accepted)
  sort.sort(current_offers, 'dateRequested', "desc")
  wishlist = list(Wishlist.objects.filter(user = request.user.get_profile()))

  hist = list(Transaction.objects.filter(status = 'confirmed', sender = request.user.get_profile()))
  
  hist_listings = Currentlist.objects.filter(user = request.user.get_profile(), status = 'closed')
  for listing in hist_listings:
    hist_as_receiver = list(Transaction.objects.filter(status = 'confirmed', current_listing = listing))
    hist.extend(hist_as_receiver)
  
  sort.sort(hist, 'dateTraded', "desc")

  if len(current_listings) == 0:
    messages.success(request, "Got any old games? Go ahead and post a listing for them.")
  if len(current_offers) == 0:
    messages.success(request, "You don't have any active offers, go ahead and browse for a new game.")
  if len(hist) == 0:
    messages.success(request, "Don't worry if your history is empty, that will fill up as soon as you complete a trade.")  

  return render(request, 'users/account_management.html', {
    'current_listings': current_listings,
    'wishlist': wishlist,
    'history': hist,
    'listing_dict': listing_dict,
    'username': request.user.username,
    'current_offers': current_offers,
    'userprofiler': userprofiler
    })

def sign_up(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  else:
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password'],)
            user_profile = UserProfile.objects.create(user = user, rating = 0, num_of_ratings = 0)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for registering %s' % user.username)
            user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
              # Login the user
              login(request, user)
              return HttpResponseRedirect('/')

        else:
            if "__all__" in form._errors:
                messages.add_message(request, messages.ERROR, form._errors['__all__'])
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))
