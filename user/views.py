from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from trades.models import *
from user.forms import LoginForm


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
