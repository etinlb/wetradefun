"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
from django.utils import unittest
from trades.models import *
from user.models import *
from django.db.models import *
from datetime import *
import sys
from itertools import chain

class Test1(unittest.TestCase):
    def setUp(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        allen = User.objects.create_user('allen', 'allen@allen.com', 'allenpassword')
        allen.save()

        bob = User.objects.create_user('bob', 'bob@bob.com', 'bobpassword')
        bob.save()

        cathy = User.objects.create_user('cathy', 'cathy@cathy.com', 'cathypassword')
        cathy.save()

        doris = User.objects.create_user('doris', 'doris@doris.com', 'dorispassword')
        doris.save()

        edward = User.objects.create_user('edward', 'edward@edward.com', 'edwardpassword')
        edward.save()

        fred = User.objects.create_user('fred', 'fred@fred.com', 'fredpassword')
        fred.save()

        graves = User.objects.create_user('graves', 'graves@graves.com', 'gravespassword')
        graves.save()

        self.allenProfile = UserProfile.objects.create(user=allen, address="allenroad", rating=3)
        self.bobProfile = UserProfile.objects.create(user=bob, address="bobroad", rating=3)
        self.cathyProfile = UserProfile.objects.create(user=cathy, address="cathyroad", rating=3)    
        self.dorisProfile = UserProfile.objects.create(user=doris, address="dorisroad", rating=3)
        self.edwardProfile = UserProfile.objects.create(user=edward, address="edwardroad", rating=3)
        self.fredProfile = UserProfile.objects.create(user=fred, address="fredroad", rating=3)
        self.gravesProfile = UserProfile.objects.create(user=graves, address="gravesroad", rating=3)



#allen, bob, cathy, and doris all make offers for gameID=11 which are listed by edward, fred, and graves. 
        self.transaction1 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction2 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 11, 11), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction3 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 12, 12), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.gravesProfile, receiver_giantBombID=11)
        self.transaction4 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction5 = Transaction.objects.create(status="pending", dateRequested=datetime(2011, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction6 = Transaction.objects.create(status="offered", dateRequested=datetime(2012, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.gravesProfile, receiver_giantBombID=11)
        self.transaction7 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction8 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction9 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.gravesProfile, receiver_giantBombID=11)
        self.transaction10 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.dorisProfile, sender_giantBombID=3, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction11 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.dorisProfile, sender_giantBombID=3, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction12 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.dorisProfile, sender_giantBombID=3, receiver=self.gravesProfile, receiver_giantBombID=11)


#graves makes an offer to everybody else's listing of gameID=12
        self.transaction13 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.allenProfile, receiver_giantBombID=12)
        self.transaction14 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.bobProfile, receiver_giantBombID=12)
        self.transaction15 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.cathyProfile, receiver_giantBombID=12)
        self.transaction16 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.dorisProfile, receiver_giantBombID=12)
        self.transaction17 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.edwardProfile, receiver_giantBombID=12)
        self.transaction18 = Transaction.objects.create(status="offered", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=12)

#to check the most traded game of all time is gameID=1
        self.transaction19 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=1, receiver=self.allenProfile, receiver_giantBombID=12)
        self.transaction20 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.bobProfile, receiver_giantBombID=12)
        self.transaction21 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.allenProfile, receiver_giantBombID=13)
        self.transaction22 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.fredProfile, receiver_giantBombID=13)
        self.transaction23 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=2, receiver=self.gravesProfile, receiver_giantBombID=13)
        self.transaction24 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=11)

#to check most wishlisted game of all time is gameID=101
        self.wishlist1 = Wishlist.objects.create(user=self.allenProfile, giantBombID=106, datePosted=datetime(2010, 10, 10))
        self.wishlist2 = Wishlist.objects.create(user=self.allenProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist3 = Wishlist.objects.create(user=self.allenProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist4 = Wishlist.objects.create(user=self.allenProfile, giantBombID=104, datePosted=datetime(2010, 10, 10))
        self.wishlist5 = Wishlist.objects.create(user=self.allenProfile, giantBombID=105, datePosted=datetime(2010, 10, 10))

        self.wishlist6 = Wishlist.objects.create(user=self.bobProfile, giantBombID=106, datePosted=datetime(2010, 10, 10))
        self.wishlist7 = Wishlist.objects.create(user=self.bobProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist8 = Wishlist.objects.create(user=self.bobProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist9 = Wishlist.objects.create(user=self.bobProfile, giantBombID=104, datePosted=datetime(2010, 10, 10))

        self.wishlist10 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=106, datePosted=datetime(2010, 10, 10))
        self.wishlist11 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist12 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))

        self.wishlist13 = Wishlist.objects.create(user=self.dorisProfile, giantBombID=106, datePosted=datetime(2010, 10, 10))
        self.wishlist14 = Wishlist.objects.create(user=self.dorisProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))

        self.wishlist15 = Wishlist.objects.create(user=self.edwardProfile, giantBombID=106, datePosted=datetime(2010, 10, 10))

    # def test1(self):
    #     #q = Transaction.objects.all().filter(sender.user="allen").order_by('-sender_giantBombID')


    #     q = Transaction.objects.filter(sender=self.allenProfile).order_by('dateRequested')
    #     r = Transaction.objects.filter(sender=self.bobProfile).order_by('dateRequested')
    #     s = list(chain(q, r))

#1.most traded games: all time
#2.hot wish-list item: the game that appears on the most wish-lists
#3.hot current listing: (how many current listings have that game)
#4.hot current listing: (the current listing with the most trade offers on it)

    def test1(self):

        i = 0
        orderedTransactionTmp = Transaction.objects.all().filter(status="confirmed")
        orderedTransaction11 = orderedTransactionTmp.order_by('receiver_giantBombID')
        orderedTransaction = list(orderedTransaction11)
        topRatedGames1 = []


        while (i != 3):
            j = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            while (j < len(orderedTransaction) - 1):
                tmp = 1
                while (orderedTransaction[j].receiver_giantBombID == orderedTransaction[j+1].receiver_giantBombID):

                    tmp = tmp + 1
                    j = j + 1

                    if j == len(orderedTransaction) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = j - maxCount + 1

                j = j + 1

            
            topRatedGames1.append(orderedTransaction[startIndex].receiver_giantBombID)

            while (maxCount != 0):
                orderedTransaction.remove(orderedTransaction[startIndex])
                maxCount = maxCount - 1

            i = i + 1


        self.assertEquals(topRatedGames1[0], 13)
        self.assertEquals(topRatedGames1[1], 12)
        self.assertEquals(topRatedGames1[2], 11) 

    def test2(self):

        orderedTransactionTmp2 = Transaction.objects.all().filter(status="confirmed")
        orderedTransaction22 = orderedTransactionTmp2.order_by('sender_giantBombID')
        orderedTransaction2 = list(orderedTransaction22)
        topRatedGames2 = []

        m = 0
        while (m != 3):
            n = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            tmpString = ""
            while (n < len(orderedTransaction2) - 1):
                tmp = 1
                while (orderedTransaction2[n].sender_giantBombID == orderedTransaction2[n+1].sender_giantBombID):

                    tmp = tmp + 1
                    n = n + 1

                    if n == len(orderedTransaction2) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = n - maxCount + 1

                n = n + 1

            topRatedGames2.append(orderedTransaction2[startIndex].sender_giantBombID)

            while (maxCount != 0):
                orderedTransaction2.remove(orderedTransaction2[startIndex])
                maxCount = maxCount - 1

            m = m + 1

        self.assertEquals(topRatedGames2[0], 3)
        self.assertEquals(topRatedGames2[1], 2)
        self.assertEquals(topRatedGames2[2], 1)

      

    def test3(self):

        orderedWishlist1 = Wishlist.objects.order_by('giantBombID')
        orderedWishlist = list(orderedWishlist1)
        topRatedWishlist = []

        m = 0
        while (m != 3):
            n = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            tmpString = ""
            while (n < len(orderedWishlist) - 1):
                tmp = 1
                while (orderedWishlist[n].giantBombID == orderedWishlist[n+1].giantBombID):

                    tmp = tmp + 1
                    n = n + 1

                    if n == len(orderedWishlist) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = n - maxCount + 1

                n = n + 1

            topRatedWishlist.append(orderedWishlist[startIndex].giantBombID)

            while (maxCount != 0):
                orderedWishlist.remove(orderedWishlist[startIndex])
                maxCount = maxCount - 1

            m = m + 1

        self.assertEquals(topRatedWishlist[0], 106)
        self.assertEquals(topRatedWishlist[1], 102)
        self.assertEquals(topRatedWishlist[2], 101)

    def test4(self):

        orderedTransactionTmp = Transaction.objects.all().filter(status="offered")
        orderedTransaction11 = orderedTransactionTmp.order_by('receiver_giantBombID', 'sender')
        orderedTransaction = list(orderedTransaction11)
        topRatedGames1 = []

        i = 0
        while (i != 1):
            j = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            while (j < len(orderedTransaction) - 1):
                tmp = 1
                while (orderedTransaction[j].receiver == orderedTransaction[j+1].receiver):

                    tmp = tmp + 1
                    j = j + 1

                    if j == len(orderedTransaction) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = j - maxCount + 1

                j = j + 1

            
            topRatedGames1.append(orderedTransaction[startIndex].receiver_giantBombID)

            while (maxCount != 0):
                orderedTransaction.remove(orderedTransaction[startIndex])
                maxCount = maxCount - 1

            i = i + 1


        self.assertEquals(topRatedGames1[0], 11)


    def test5(self):
        orderedTransactionTmp = Transaction.objects.all().filter(status="offered")
        orderedTransaction11 = orderedTransactionTmp.order_by('receiver_giantBombID', 'sender')
        orderedTransaction = list(orderedTransaction11)
        topRatedGames1 = []

        i = 0
        while (i != 1):
            j = 0
            maxCount = 0
            startIndex = 0
            tmp = 0
            while (j < len(orderedTransaction) - 1):
                tmp = 1
                while (orderedTransaction[j].sender == orderedTransaction[j+1].sender):

                    tmp = tmp + 1
                    j = j + 1

                    if j == len(orderedTransaction) - 1:
                        break

                if (tmp > maxCount):
                    maxCount = tmp
                    startIndex = j - maxCount + 1

                j = j + 1

            
            topRatedGames1.append(orderedTransaction[startIndex].receiver_giantBombID)

            while (maxCount != 0):
                orderedTransaction.remove(orderedTransaction[startIndex])
                maxCount = maxCount - 1

            i = i + 1


        self.assertEquals(topRatedGames1[0], 12)