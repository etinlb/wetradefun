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
from user import sort

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

        self.HaloGame = Game.objects.create(platform="XBOX", image_url="", name="Halo", giant_bomb_id=2600, num_of_listings=0)
        self.StarcraftGame = Game.objects.create(platform="PC", image_url="", name="Starcraft", giant_bomb_id=13062, num_of_listings=0)
        self.CallOfDutyGame = Game.objects.create(platform="XBOX", image_url="", name="CallOfDuty", giant_bomb_id=1629, num_of_listings=0)
        self.PortalGame = Game.objects.create(platform="PC", image_url="", name="Portal", giant_bomb_id=21170, num_of_listings=0)
        self.AssassinsCreedGame = Game.objects.create(platform="XBOX", image_url="", name="AssassinsCreed", giant_bomb_id=2950, num_of_listings=0)


#allen, bob, cathy, and doris all make offers for gameID=11 which are listed by edward, fred, and graves. 

        self.transaction1 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction2 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2012, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction3 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2011, 10, 11), sender=self.allenProfile, sender_game=self.PortalGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction4 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2013, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction5 = Transaction.objects.create(status="pending", dateTraded=datetime.date(2015, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction6 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2014, 10, 11), sender=self.bobProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction7 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction8 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction9 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)
        self.transaction10 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.edwardProfile, receiver_game=self.HaloGame)
        self.transaction11 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.fredProfile, receiver_game=self.HaloGame)
        self.transaction12 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.dorisProfile, sender_game=self.CallOfDutyGame, receiver=self.gravesProfile, receiver_game=self.HaloGame)


#graves makes an offer to everybody else's listing of gameID=12
        self.transaction13 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.PortalGame)
        self.transaction14 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction15 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.cathyProfile, receiver_game=self.PortalGame)
        self.transaction16 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.dorisProfile, receiver_game=self.PortalGame)
        self.transaction17 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.edwardProfile, receiver_game=self.PortalGame)
        self.transaction18 = Transaction.objects.create(status="offered", dateTraded=datetime.date(2010, 10, 11), sender=self.gravesProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.PortalGame)

#to check the most traded game of all time is gameID=1
        self.transaction19 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.allenProfile, receiver_game=self.PortalGame)
        self.transaction20 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.AssassinsCreedGame, receiver=self.bobProfile, receiver_game=self.PortalGame)
        self.transaction21 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.allenProfile, receiver_game=self.CallOfDutyGame)
        self.transaction22 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.fredProfile, receiver_game=self.CallOfDutyGame)
        self.transaction23 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.StarcraftGame, receiver=self.gravesProfile, receiver_game=self.CallOfDutyGame)
        self.transaction24 = Transaction.objects.create(status="confirmed", dateTraded=datetime.date(2010, 10, 11), sender=self.cathyProfile, sender_game=self.PortalGame, receiver=self.fredProfile, receiver_game=self.StarcraftGame)

#to check most wishlisted game of all time is gameID=101
        self.wishlist1 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist2 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist3 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist4 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist5 = Wishlist.objects.create(user=self.allenProfile, wishlist_game=self.PortalGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist6 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist7 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist8 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist9 = Wishlist.objects.create(user=self.bobProfile, wishlist_game=self.CallOfDutyGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist10 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist11 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist12 = Wishlist.objects.create(user=self.cathyProfile, wishlist_game=self.AssassinsCreedGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist13 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))
        self.wishlist14 = Wishlist.objects.create(user=self.dorisProfile, wishlist_game=self.StarcraftGame, datePosted=datetime.date(2010, 10, 10))

        self.wishlist15 = Wishlist.objects.create(user=self.edwardProfile, wishlist_game=self.HaloGame, datePosted=datetime.date(2010, 10, 10))

    def test_sort_desc(self):
        h = list(Transaction.objects.filter(sender=self.allenProfile))
        bob_h = list(Transaction.objects.filter(sender=self.bobProfile))
        h.extend(bob_h)

        print "\n*** Unsorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        sort.sort(h, 'dateTraded', "desc")

        print "\n*** Desc Sorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        self.assertFalse(0) # True = see print stmts

    def test_sort_asc(self):
        h = list(Transaction.objects.filter(sender=self.allenProfile).order_by('-dateTraded'))
        bob_h = list(Transaction.objects.filter(sender=self.bobProfile).order_by('-dateTraded'))
        h.extend(bob_h)

        print "\n*** Unsorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        sort.sort(h, 'dateTraded', "asc")

        print "\n*** Asc Sorted List ***"
        for i in h:
            print str(i.sender.user) + "\t" + str(i.dateTraded)

        self.assertFalse(0) # True = see print stmts

    #1.most traded games: all time
    #2.hot wish-list item: the game that appears on the most wish-lists
    #3.hot current listing: (how many current listings have that game)
    #4.hot current listing: (the current listing with the most trade offers on it)

    # def test1(self):
    #     orderedTransactionTmp = Transaction.objects.filter(status="confirmed")
    #     orderedTransactionTmp.order_by('reciever_game__giant_bomb_id')
    #     orderedTransaction = list(orderedTransactionTmp)
    #     topRatedGames1 = []

    #     i = 0
    #     while (i != 3):
    #         j = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (j < len(orderedTransaction) - 1):
    #             tmp = 1
    #             while (orderedTransaction[j].receiver_game == orderedTransaction[j+1].receiver_game):

    #                 tmp = tmp + 1
    #                 j = j + 1

    #                 if j == len(orderedTransaction) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = j - maxCount + 1

    #             j = j + 1
       
    #         topRatedGames1.append(orderedTransaction[startIndex].receiver_game.name)

    #         while (maxCount != 0):
    #             orderedTransaction.remove(orderedTransaction[startIndex])
    #             maxCount = maxCount - 1

    #         i = i + 1
   


    #     self.assertEquals(topRatedGames1[0], "CallOfDuty")
    #     self.assertEquals(topRatedGames1[1], "Portal")
    #     self.assertEquals(topRatedGames1[2], "Starcraft")


    # def test2(self):
    #     orderedTransactionTmp = Transaction.objects.filter(status="confirmed")
    #     orderedTransaction1 = orderedTransactionTmp.order_by('reciever_game__giant_bomb_id')
    #     orderedTransaction = list(orderedTransaction1)
    #     topRatedGames1 = []

    #     i = 0
    #     while (i != 3):
    #         j = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (j < len(orderedTransaction) - 1):
    #             tmp = 1
    #             while (orderedTransaction[j].receiver_game == orderedTransaction[j+1].receiver_game):

    #                 tmp = tmp + 1
    #                 j = j + 1

    #                 if j == len(orderedTransaction) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = j - maxCount + 1

    #             j = j + 1
       
    #         topRatedGames1.append(orderedTransaction[startIndex].receiver_game.name)

    #         while (maxCount != 0):
    #             orderedTransaction.remove(orderedTransaction[startIndex])
    #             maxCount = maxCount - 1

    #         i = i + 1
   


    #     self.assertEquals(topRatedGames1[0], "CallOfDuty")
    #     self.assertEquals(topRatedGames1[1], "Portal")
    #     self.assertEquals(topRatedGames1[2], "Starcraft")
        # orderedTransactionTmp = Transaction.objects.filter(status="confirmed")
        # orderedTransactionTmp.order_by('sender_game__giant_bomb_id')
        # orderedTransaction = list(orderedTransactionTmp)
        # topRatedGames1 = []

        # i = 0
        # while (i != 3):
        #     j = 0
        #     maxCount = 0
        #     startIndex = 0
        #     tmp = 0
        #     while (j < len(orderedTransaction) - 1):
        #         tmp = 1
        #         while (orderedTransaction[j].sender_game == orderedTransaction[j+1].sender_game):

        #             tmp = tmp + 1
        #             j = j + 1

        #             if j == len(orderedTransaction) - 1:
        #                 break

        #         if (tmp > maxCount):
        #             maxCount = tmp
        #             startIndex = j - maxCount + 1

        #         j = j + 1
       
        #     topRatedGames1.append(orderedTransaction[startIndex].sender_game.name)

        #     while (maxCount != 0):
        #         orderedTransaction.remove(orderedTransaction[startIndex])
        #         maxCount = maxCount - 1

        #     i = i + 1
   
       
        # self.assertEquals(topRatedGames1[0], "Starcraft")
        # self.assertEquals(topRatedGames1[1], "AssassinsCreed")
        # self.assertEquals(topRatedGames1[2], "Portal") 

      

    # def test3(self):

    #     orderedWishlist1 = Wishlist.objects.order_by('giantBombID')
    #     orderedWishlist = list(orderedWishlist1)
    #     topRatedWishlist = []

    #     m = 0
    #     while (m != 3):
    #         n = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (n < len(orderedWishlist) - 1):
    #             tmp = 1
    #             while (orderedWishlist[n].giantBombID == orderedWishlist[n+1].giantBombID):

    #                 tmp = tmp + 1
    #                 n = n + 1

    #                 if n == len(orderedWishlist) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = n - maxCount + 1

    #             n = n + 1

    #         topRatedWishlist.append(orderedWishlist[startIndex].giantBombID)

    #         while (maxCount != 0):
    #             orderedWishlist.remove(orderedWishlist[startIndex])
    #             maxCount = maxCount - 1

    #         m = m + 1

    #     self.assertEquals(topRatedWishlist[0], 106)
    #     self.assertEquals(topRatedWishlist[1], 102)
    #     self.assertEquals(topRatedWishlist[2], 101)

    # def test4(self):

    #     orderedTransactionTmp = Transaction.objects.all().filter(status="offered")
    #     orderedTransaction11 = orderedTransactionTmp.order_by('receiver_game', 'sender')
    #     orderedTransaction = list(orderedTransaction11)
    #     topRatedGames1 = []

    #     i = 0
    #     while (i != 2):
    #         j = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (j < len(orderedTransaction) - 1):
    #             tmp = 1
    #             while (orderedTransaction[j].receiver == orderedTransaction[j+1].receiver):

    #                 tmp = tmp + 1
    #                 j = j + 1

    #                 if j == len(orderedTransaction) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = j - maxCount + 1

    #             j = j + 1

            
    #         topRatedGames1.append(orderedTransaction[startIndex].receiver_game)

    #         while (maxCount != 0):
    #             orderedTransaction.remove(orderedTransaction[startIndex])
    #             maxCount = maxCount - 1

    #         i = i + 1


    #     self.assertEquals(topRatedGames1[0], 11)
    #     #self.assertEquals(topRatedGames1[1], 12)


    # def test5(self):
    #     orderedTransactionTmp = Transaction.objects.all().filter(status="offered")
    #     orderedTransaction11 = orderedTransactionTmp.order_by('receiver_game', 'sender')
    #     orderedTransaction = list(orderedTransaction11)
    #     topRatedGames1 = []

    #     i = 0
    #     while (i != 2):
    #         j = 0
    #         maxCount = 0
    #         startIndex = 0
    #         tmp = 0
    #         while (j < len(orderedTransaction) - 1):
    #             tmp = 1
    #             while (orderedTransaction[j].sender == orderedTransaction[j+1].sender):

    #                 tmp = tmp + 1
    #                 j = j + 1

    #                 if j == len(orderedTransaction) - 1:
    #                     break

    #             if (tmp > maxCount):
    #                 maxCount = tmp
    #                 startIndex = j - maxCount + 1

    #             j = j + 1

            
    #         topRatedGames1.append(orderedTransaction[startIndex].receiver_game)

    #         while (maxCount != 0):
    #             orderedTransaction.remove(orderedTransaction[startIndex])
    #             maxCount = maxCount - 1

    #         i = i + 1


    #     self.assertEquals(topRatedGames1[0], 12)
    #     #self.assertEquals(topRatedGames1[1], 11)