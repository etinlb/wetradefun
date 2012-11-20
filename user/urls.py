from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
  ('^/sign_in$', 'user.views.sign_in'),
)