import datetime, random, sha

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from trades.forms import RegistrationForm

from trades.models import *
import search as s
from trades.forms import SearchForm

def account_management(request, userID)
	try:
      user_profile = UserProfile.objects.get(id = userID)
  except Currentlist.DoesNotExist:
      user_profile = None

  current_list = Currentlist.objects.get(user = userID)
  wish_list = Wishlist.objects.get(user = userID)
  trans_hist = Transaction.objects.get(status = "completed", sender = userID)
  trans_hist2 = Transaction.objects.get(status = "completed", receiver = userID)