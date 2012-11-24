from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from user.forms import RegistrationForm, LoginForm

from trades.models import *

from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

import search as s
# from trades.forms import SearchForm

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

def account_management(request, userID):
  try:
    user_profile = UserProfile.objects.get(id = userID)
  except Currentlist.DoesNotExist:
    user_profile = None

  try: 
    current_listings = Currentlist.objects.get(user = user_id)
  except Currentlist.DoesNotExist:
    current_listings = None

  try: 
    wish_list = Wishlist.objects.get(user = user_id)
  except Wishlist.DoesNotExist:
    wish_list = None

  # decide on the different statuses
  try:
    hist_sender = Transaction.objects.get(status = "completed", sender = user_id)
  except Transaction.DoesNotExist:
    hist_sender = None

  try:
    hist_receiver = Transaction.objects.get(status = "completed", receiver = user_id)
  except Transaction.DoesNotExist:
    hist_sender = None

  hist = dict(hist_sender.items() + hist_receiver.items())

  return render_to_response('users/account_management.html')



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
            if "__all__" in form._errors:
                messages.add_message(request, messages.ERROR, form._errors['__all__'])
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    },
     context_instance=RequestContext(request))
    
