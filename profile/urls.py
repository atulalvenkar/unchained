from django.conf.urls import patterns, include, url
from profile import views

urlpatterns = patterns('',
    url(r'^show/$', views.show, name="profile_show"),
    url(r'^show/([\w\d]{32})/$', views.show_other, name="profile_show_others"),
    url(r'^create/$', views.create, name="profile_create")
)
