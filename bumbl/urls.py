from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^__page/([0-9]+)/(.*)$', 'bumble.bumbl.views.page'),
    url(r'^(.*)$', 'bumble.bumbl.views.entry')
)
