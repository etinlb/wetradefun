from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^search/$','trades.views.search' ),
    url(r'^game/(?P<game_id>\d+)/$', 'trades.views.game_details'),
    url(r'^add_to_wish_list/$', 'trades.views.add_to_wish_list'),
    url(r'^remove_from_wish_list/$', 'trades.views.remove_from_wish_list'),
    url(r'^make_offer/$', 'trades.views.make_offer'),
    url(r'^add_listing/$', 'trades.views.add_listing'),
    url(r'^remove_listing/$', 'trades.views.remove_listing')
)