from django.template import Context, loader
# from polls.models import Poll
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
import search as s
from django.db.models import Avg, Max, Min, Count

from trades.models import *
from users.sort import *
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


	mostTradedGames = getMostTradedGames()
    mostWishlistedGames = getMostWishlistedGames()
    mostListedGames = getMostListedGames()

    return render(request, 'base.html', {
        'most_traded_games': mostTradedGames,
        'most_Wishlisted_Games': mostWishlistedGames,
        'most_Listed_Games': mostListedGames,
        'username':request.user.username,
        })
	


def getMostTradedGames():

    orderedTransaction = []

    orderedTransactionTmp = Transaction.objects.all()
    for transactionobjects in orderedTransactionTmp:
        if transactionobjects.status == "confirmed":
            orderedTransaction.append(transactionobjects.sender_game)
            orderedTransaction.append(transactionobjects.receiver_game)

    sort(orderedTransaction, 'name', 'desc')
    topRatedGames = []

    i = 0
    while (i != 4):
        j = 0
        maxCount = 0
        startIndex = 0
        tmp = 0
        while (j < len(orderedTransaction) - 1):
            tmp = 1
            while (orderedTransaction[j] == orderedTransaction[j+1]):

                tmp = tmp + 1
                j = j + 1

                if j == len(orderedTransaction) - 1:
                    break

            if (tmp > maxCount):
                maxCount = tmp
                startIndex = j - maxCount + 1

            j = j + 1
   
        topRatedGames.append(orderedTransaction[startIndex].name)

        while (maxCount != 0):
            orderedTransaction.remove(orderedTransaction[startIndex])
            maxCount = maxCount - 1


        i = i + 1
    return topRatedGames

def getMostWishlistedGames():

    orderedWishlist = []
    orderedWishlistTmp = Wishlist.objects.all()
    #orderedWishlistTmp.order_by('wishlist_game')
    #orderedWishlist = list(orderedWishlistTmp)
    for wishlistobjects in orderedWishlistTmp:
        orderedWishlist.append(wishlistobjects.wishlist_game)

    sort(orderedWishlist, 'name', 'desc')

    topRatedWishlist = []

    m = 0
    while (m != 5):
        n = 0
        maxCount = 0
        startIndex = 0
        tmp = 0
        while (n < len(orderedWishlist) - 1):
            tmp = 1
            while (orderedWishlist[n] == orderedWishlist[n+1]):

                tmp = tmp + 1
                n = n + 1

                if n == len(orderedWishlist) - 1:
                    break

            if (tmp > maxCount):
                maxCount = tmp
                startIndex = n - maxCount + 1

            n = n + 1

        topRatedWishlist.append(orderedWishlist[startIndex])

        while (maxCount != 0):
            orderedWishlist.remove(orderedWishlist[startIndex])
            maxCount = maxCount - 1

        m = m + 1

    return topRatedWishlist

def getMostListedGames():

    orderedListing = Game.objects.all()
    sort(orderedListing, 'num_of_listings', 'desc')
    topRatedListings = []
    j = 0

    while (j < len(orderedListing) - 1):
        
        topRatedListings.append(orderedListing[j].name)
        j = j + 1

    return topRatedListings



