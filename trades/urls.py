from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^$', 'user.views.sign_in'),
    url(r'^search/(?P<query>\w+)/$','trades.views.search' ),
    url(r'^$', 'trades.views.sign_up'),
    url(r'^users/sign_in$', 'user.views.sign_in'),
    url(r'^game/(?P<game_id>\d+)/$', 'trades.views.game_details')

)