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

    # def test_checkingstuff(self):


    #1.most traded games: all time
    #2.hot wish-list item: the game that appears on the most wish-lists
    #3.hot current listing: (how many current listings have that game)
    #4.hot current listing: (the current listing with the most trade offers on it)

    #allen, bob, and cathy all make offers for gameID=11 which are listed by edward, fred, and graves. doris is noob and doesnt do anything.
        self.transaction1 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction2 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 11, 11), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction3 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 12, 12), dateTraded="N/A", sender=self.allenProfile, sender_giantBombID=1, receiver=self.gravesProfile, receiver_giantBombID=11)
        self.transaction4 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction5 = Transaction.objects.create(status="pending", dateRequested=datetime(2011, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction6 = Transaction.objects.create(status="pending", dateRequested=datetime(2012, 10, 10), dateTraded="N/A", sender=self.bobProfile, sender_giantBombID=2, receiver=self.gravesProfile, receiver_giantBombID=11)
        self.transaction7 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.edwardProfile, receiver_giantBombID=11)
        self.transaction8 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.fredProfile, receiver_giantBombID=11)
        self.transaction9 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.gravesProfile, receiver_giantBombID=11)

    #graves makes an offer to everybody else's listing of gameID=12
        self.transaction10 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.allenProfile, receiver_giantBombID=12)
        self.transaction11 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.bobProfile, receiver_giantBombID=12)
        self.transaction12 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.cathyProfile, receiver_giantBombID=12)
        self.transaction13 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.dorisProfile, receiver_giantBombID=12)
        self.transaction14 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.edwardProfile, receiver_giantBombID=12)
        self.transaction15 = Transaction.objects.create(status="pending", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.gravesProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=12)

    #to check the most traded game of all time is gameID=1
        self.transaction16 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=1, receiver=self.allenProfile, receiver_giantBombID=11)
        self.transaction17 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=1, receiver=self.bobProfile, receiver_giantBombID=12)
        self.transaction18 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=1, receiver=self.allenProfile, receiver_giantBombID=13)
        self.transaction19 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=2, receiver=self.fredProfile, receiver_giantBombID=14)
        self.transaction20 = Transaction.objects.create(status="confirmed", dateRequested=datetime(2010, 10, 10), dateTraded="N/A", sender=self.cathyProfile, sender_giantBombID=3, receiver=self.gravesProfile, receiver_giantBombID=15)

    #to check most wishlisted game of all time is gameID=101
        self.wishlist1 = Wishlist.objects.create(user=self.allenProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist2 = Wishlist.objects.create(user=self.allenProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist3 = Wishlist.objects.create(user=self.allenProfile, giantBombID=103, datePosted=datetime(2010, 10, 10))
        self.wishlist4 = Wishlist.objects.create(user=self.allenProfile, giantBombID=104, datePosted=datetime(2010, 10, 10))
        self.wishlist5 = Wishlist.objects.create(user=self.allenProfile, giantBombID=105, datePosted=datetime(2010, 10, 10))

        self.wishlist6 = Wishlist.objects.create(user=self.bobProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist7 = Wishlist.objects.create(user=self.bobProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist8 = Wishlist.objects.create(user=self.bobProfile, giantBombID=103, datePosted=datetime(2010, 10, 10))
        self.wishlist9 = Wishlist.objects.create(user=self.bobProfile, giantBombID=104, datePosted=datetime(2010, 10, 10))

        self.wishlist10 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist11 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))
        self.wishlist12 = Wishlist.objects.create(user=self.cathyProfile, giantBombID=103, datePosted=datetime(2010, 10, 10))

        self.wishlist13 = Wishlist.objects.create(user=self.dorisProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))
        self.wishlist14 = Wishlist.objects.create(user=self.dorisProfile, giantBombID=102, datePosted=datetime(2010, 10, 10))

        self.wishlist15 = Wishlist.objects.create(user=self.edwardProfile, giantBombID=101, datePosted=datetime(2010, 10, 10))

        
    def test_join_lists(self):
        q = list(Transaction.objects.filter(sender=self.allenProfile).order_by('dateRequested'))
        r = list(Transaction.objects.filter(sender=self.bobProfile).order_by('dateRequested'))
        q.extend(r)
        self.assertEquals(q[3].sender.user, 1)

        #def test1(self):
        #   q = Wishlist.objects.all().annotate(Avg('giantBombID'))
        #   self.assertEquals(q[0], 3)

        #def test2(self):
        #r = Transaction.objects.all().aggregate(Avg('receiver_giantBombID'))
        #self.assertEquals(r, 3)        

        #self.assertEquals(q, 121231)
        #q = Wishlist.objects.all().annotate(maxnumber=Count('giantBombID'))

        #mostfrequent = Wishlist.objects.values('giantBombID').annotate(Count('id')).order_by()

        #self.assertEquals(Wishlist.objects.size(), 14)

        #for i in Wishlist.objects.size:

        #self.assertEquals(q[0].maxnumber, 4)

        #self.assertEquals(mostfrequent, 4)