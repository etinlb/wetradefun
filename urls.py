from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^trades/', include('trades.urls')),
    url(r'^users/', include('user.urls')),
    url(r'^$', 'views.homepage'),
    url(r'^how_to_use', 'views.how_to_use'),
    url(r'^contact_us', 'views.contact_us'),
    url(r'^no_game_found', 'views.no_game_found'),
)