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

def sign_out(request):
  logout(request)
  return render(request, 'base.html')

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

def account_management(request):
  listing_list = {}
  listing_dict = {}
  current_listings = list(Currentlist.objects.filter(user = request.user.get_profile()).order_by('-datePosted'))
  for idx, listing in enumerate(current_listings):
      listing_dict[listing] = list(Transaction.objects.filter(Q(status = 'pending') \
        & Q(receiver = request.user.get_profile()) & Q(receiver_game = listing.game_listed )))
      # listing_list[idx] = listing_dict 
      # listing_dict['offers'] = 
  #assert false
  current_offers = list(Transaction.objects.filter(Q(status = 'pending') \
    & Q(sender = request.user.get_profile())))

  wishlist = list(Wishlist.objects.filter(user = request.user.get_profile()))

  hist = list(Transaction.objects.filter(status = 'confirmed', sender = request.user.get_profile()).order_by('-dateTraded'))
  hist_as_receiver = list(Transaction.objects.filter(status = 'confirmed', receiver = request.user.get_profile()).order_by('-dateTraded'))
  hist.extend(hist_as_receiver)
  sort.sort(hist, 'dateTraded', "desc")

  return render(request, 'users/account_management.html', {
    'current_listings': current_listings,
    'wishlist': wishlist,
    'history': hist,
    'listing_dict':listing_dict,
    'username':request.user.username,
    'current_offers':current_offers
    })

def sign_up(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            user = User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password'],)
            user_profile = UserProfile(user = user)
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, 'Thanks for registering %s' % user.username)
            user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
              # Login the user
              login(request, user)

        else:
            if "__all__" in form._errors:
                messages.add_message(request, messages.ERROR, form._errors['__all__'])
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))
