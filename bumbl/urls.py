from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^__page/([0-9]+)/(.*)$', views.page, name="page"),
    url(r'^(.*)$', views.entry, name="entry")
]
