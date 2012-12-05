from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from user.forms import *
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

def forget(request):
  # If it's 
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')
  else:
    if request.method == 'POST': # If the form has been submitted...
        form = ForgetForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            try:
                user = User.objects.get(username=form.cleaned_data['username'],email=form.cleaned_data['email'])
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Username and Email does not exist')
                return render_to_response('users/forget.html', {'form': form,},context_instance=RequestContext(request))
            user.set_password("WeTradeFun")
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password is reset to WeTradeFun')
        else:
            messages.add_message(request, messages.ERROR, 'Your form is incorrect')
    else:
        form = ForgetForm() # An unbound form
  return render_to_response('users/forget.html', {'form': form,},context_instance=RequestContext(request))

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
  # if request.method == 'POST':
  #   form = LoginForm(request.POST)
  #   if form.is_valid():
  #     newPassword = form.get_cleaned_data['new_password']
  listing_dict = {}
  accepted_offer_dict = {}
  userprofiler = request.user.get_profile()
  current_listings = list(Currentlist.objects.filter(user = request.user.get_profile(), status = 'open').order_by('-datePosted'))
  for idx, listing in enumerate(current_listings):
    listing_dict[listing] = list(Transaction.objects.filter(status = 'offered', current_listing = listing))
    try:
      accepted_offer_dict[listing] = Transaction.objects.get(status = 'accepted', current_listing = listing)
    except Transaction.DoesNotExist:
       accepted_offer_dict[listing] = []


  # assert False  

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
    'userprofiler': userprofiler,
    'accepted_offer_dict':accepted_offer_dict
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

@login_required(login_url='/users/sign_in/')
def edit_email(request):
  if request.is_ajax():
    old_email = request.GET.get('oemail')
    new_email = request.GET.get('nemail')
    confirmed_email = request.GET.get('cemail')
    current_user = request.user.get_profile().user

    if(old_email != current_user.email):
      message = "Old email is incorrect!"
    elif (new_email != confirmed_email):
      message = "New emails don't match!"
    else:
      current_user.email = new_email
      current_user.save()
      message = "Your email has been sucessfully changed"
  else:
    message = "Not AJAX"


  messages.success(request, message)
  return HttpResponse(message)

@login_required(login_url='/users/sign_in/')
def edit_password(request):
  if request.is_ajax():
    old_password = request.GET.get('opassword')
    new_password = request.GET.get('npassword')
    confirmed_password = request.GET.get('cpassword')
    current_user = request.user.get_profile().user

    if not current_user.check_password(old_password):
      message = "Old password is incorrect!"
    elif new_password != confirmed_password:
      message = "New passwords don't match!"
    else:
      current_user.set_password(new_password)
      current_user.save()
      message = "Your password has been sucessfully changed"
  else:
    message = "Not AJAX"

  messages.success(request, message)

  return HttpResponse(message)
