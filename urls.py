from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^trades/$', 'trades.views.index'),
	(r'^trades/save/(?P<users_name>\w+)/$', 'trades.views.save'),
	(r'^trades/load/(?P<users_id>\d+)/$', 'trades.views.load'),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
)
