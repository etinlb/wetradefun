from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^search/(?P<query>\w+)/$','trades.views.search' ),
    url(r'^game/(?P<game_id>\d+)/$', 'trades.views.game_details')

)