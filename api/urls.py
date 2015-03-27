from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
  url(r'^createchecksum/$', views.createchecksum, name='createchecksum'),
  url(r'^verifychecksum/$', views.verifychecksum, name='verifychecksum'),
)
