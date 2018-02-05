from django.conf.urls import url
from django.contrib import admin
from . import views 

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^friends$', views.dashboard),
  url(r'^users/(?P<id>\d+)$', views.profile),
  url(r'^users/add/(?P<id>\d+)$', views.addfriend),
  url(r'^users/remove/(?P<id>\d+)$', views.removefriend),
]