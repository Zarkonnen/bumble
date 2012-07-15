from django.conf.urls.defaults import patterns, include, url
from bumble import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bumble.views.home', name='home'),
    # url(r'^bumble/', include('bumble.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^%s(?P<path>.*)$' % settings.MEDIA_URL, 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}))

urlpatterns += patterns('',
                        url(r'^', include('bumble.bumbl.urls')))
