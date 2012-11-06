from django.http import HttpResponse
from trades.models import Users, Games, Wishlists, Currentlists, Makeoffers, Getoffers, Gamecomments, Messages, Userrating, Gameratings

def index(request):
    return HttpResponse("Hello, world. You're at the trades index.")

def save(request, users_name):
    u=Users(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)