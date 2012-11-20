from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^$', 'trades.views.sign'),
    (r'^trades/$', 'trades.views.index'),
	(r'^trades/save/(?P<users_name>\w+)/$', 'trades.views.save'),
	(r'^trades/load/(?P<users_id>\d+)/$', 'trades.views.load'),
	(r'^trades/search_form/$', 'trades.views.search_form'),
	(r'^trades/post_request/$', 'trades.views.post_request'),
	(r'^trades/search_game/$', 'trades.views.search_game'),
	(r'^trades/get_request/$', 'trades.views.get_request'),
)