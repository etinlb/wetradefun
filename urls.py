from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^trades/', include('trades.urls')),
    url(r'^users/', include('user.urls')),
    url(r'^$', 'views.home'),
    url(r'^how_to_use', 'views.how_to_use'),
    url(r'^contact_us', 'views.contact_us'),
    url(r'^no_game_found', 'views.no_game_found'),
 # (r'^trades/$', 'trades.views.index'),
# (r'^trades/save/(?P<users_name>\w+)/$', 'trades.views.save'),
# (r'^trades/load/(?P<users_id>\d+)/$', 'trades.views.load'),
# (r'^trades/search_form/$', 'trades.views.search_form'),
# (r'^trades/post_request/$', 'trades.views.post_request'),
# (r'^trades/search_game/$', 'trades.views.search_game'),
# (r'^trades/get_request/$', 'trades.views.get_request'),
 # ('^$', 'django.views.generic.simple.direct_to_template',
 # {'template': 'home.html'}),
 # ('^gamedetails/(?P<game_id>\d+)','trades.views.gameDetails' ),
 # (r'^trades/search/$', 'trades.views.search'),
 # (r'^trades/game/$', 'exampleview.gamepage'),
 # (r'^trades/account$', 'exampleview.account'),

)