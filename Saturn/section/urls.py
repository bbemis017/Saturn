from django.conf.urls import url
from section import views

urlpatterns = [
	url(r'^summary/add/$', views.create_summary),
	url(r'^summary/edit/$', views.edit_summary),
]
