from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response

from trades.models import UserProfile

def index(request):
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user_profile = UserProfile(user = user, account='account', address='address', rating=1)
    user_profile.save()
    return render_to_response('users/sign.html',)

# def index(request):
#     return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=UserProfile(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)