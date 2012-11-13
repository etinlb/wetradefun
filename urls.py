from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
    ('^detail/(?P<game_id>\d+)','trades.views.gameDetail' ),
    (r'^trades/search/$', 'trades.views.search'),
)
