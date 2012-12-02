from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^sign_up', 'user.views.sign_up'),
    url(r'^sign_in', 'user.views.sign_in'),
    url(r'^account_management', 'user.views.account_management'),
    url(r'^sign_out', 'user.views.sign_out'),
)