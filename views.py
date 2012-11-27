from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
import search as s
from django.db.models import Avg, Max, Min, Count

from trades.models import *
# def index(request):
#     latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#     return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})

def searchresults(request):
    return HttpResponse("You're looking at the search results.")


# This big pro homepage should have (ideally):

#1.most traded games: all time
#2.hot wish-list item: the game that appears on the most wish-lists
#3.hot current listing: (how many current listings have that game)
#4.hot current listing: (the current listing with the most trade offers on it)
def homepage(request):
	#1
	IDofMax = 0
	numofMax = 0

	#filter makes sure it only processes accepted transactions
	#values makes sure it treats all giantbombIDs that are equivalent as unique
	#annotate is for counting the # of ids
	#order_by orders them you idiot.. 
	sortedBySenderHist = Transaction.objects.filter(status__gt='accepted').values('sender_giantBombID').annotate(Count('id')).order_by()
	sortedByReceiverHist = Transaction.objects.filter(status__gt='accepted').values('receiver_giantBombID').annotate(Count('id')).order_by()

	#2
	mostFreqOnWishList = Wishlist.objects.values('giantBombID').annotate(Count('id')).order_by()

	#3
	sortedByReceiverPend1 = Transaction.objects.filter(status__gt='pending').values('receiver_giantBombID', 'sender').annotate(Count('id')).order_by()

	#4
	sortedByReceiverPend2 = Transaction.objects.filter(status__gt='pending').values('receiver_giantBombID', 'receiver').annotate(Count('id')).order_by()

	



	return render_to_response('base.html')


