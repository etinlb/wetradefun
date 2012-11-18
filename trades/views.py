import datetime, random, sha

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404


from trades.models import UserProfile
from trades.forms import RegistrationForm

def sign(request):
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
            return HttpResponse("You save a user. Please load his name by using id %s.")
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response('users/sign.html', {
        'form': form,
    })

# def index(request):
#     return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=UserProfile(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

def gamepage(request):
  gameDict = {'genres': 'awesome', 'name': 'Ratchet & Clank: Up Your Arsenal', \
  'deck': 'Ratchet & Clank:  Up Your Arsenal is the third game in the Ratchet \
  and Clank series. It is also the first to include online play.', \
  'image': 'http://media.giantbomb.com/uploads/8/87209/1974402-box_racuya_super.png', \
  'original_release_date': '2004-11-03', 'id': '4966', 'platforms': 'PS3'}
  currentNumOfListing = '1000'
  #note platfrom may be a list
  return render_to_response('gamePage.html', {'game':gameDict, 'numberOfListing':currentNumOfListing})