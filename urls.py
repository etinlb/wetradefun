from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^trades/$', 'trades.views.index'),
	(r'^trades/save/(?P<users_name>\w+)/$', 'trades.views.save'),
	(r'^trades/load/(?P<users_id>\d+)/$', 'trades.views.load'),
	(r'^trades/search_form/$', 'trades.views.search_form'),
	(r'^trades/search/$', 'trades.views.search'),
	(r'^trades/get_json/$', 'trades.views.get_json'),
	(r'^trades/search_game/$', 'trades.views.search_game'),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
)
