from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$', 'trades.views.sign'),
    url(r'^/search/(?P<query>\w+)/$','trades.views.search' ),
    ('^$', 'trades.views.sign_up'),
    ('^game$', 'trades.views.gamepage')

)