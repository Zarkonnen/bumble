from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    
    url(r'^(.*)$', 'bumble.bumbl.views.entry')
)
