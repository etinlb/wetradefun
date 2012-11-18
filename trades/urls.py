from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^$', 'trades.views.sign_up'),
    ('^users/sign_in$', 'trades.views.sign_up'),
)