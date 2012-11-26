from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import Http404
import search as s

def home(request):
  return render(request,'base.html')
