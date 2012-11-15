from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^', include('trades.urls')),
    (r'^trades/$', 'trades.views.index'),
	(r'^trades/save/(?P<users_name>\w+)/$', 'trades.views.save'),
	(r'^trades/load/(?P<users_id>\d+)/$', 'trades.views.load'),
	(r'^trades/search_form/$', 'trades.views.search_form'),
	(r'^trades/post_request/$', 'trades.views.post_request'),
	(r'^trades/search_game/$', 'trades.views.search_game'),
	(r'^trades/get_request/$', 'trades.views.get_request'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
    ('^detail/(?P<game_id>\d+)','trades.views.gameDetail' ),
    (r'^trades/search/$', 'trades.views.search'),
)
