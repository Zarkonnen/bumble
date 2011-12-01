from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('bumble.bumbl.views',
    
    url(r'^(.*)$', 'entry')
)
