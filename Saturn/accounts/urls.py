from django.conf.urls import url
from accounts import views

urlpatterns = [
	url(r'^signup/$', views.signup),
	url(r'^signin/$', views.signin),
        url(r'^reset_password/$', views.reset_password),
]
