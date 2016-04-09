from django.conf.urls import url
from accounts import views

urlpatterns = [
	url(r'^signup/$', views.signup),
	url(r'^login/$', views.signin),
	url(r'^activate/$', views.activate),
	url(r'^verification/$', views.send_verification_email),
    url(r'^reset_password/$', views.reset_password),
    url(r'^profile/$', views.profile),
    url(r'^sites/$', views.sites),
    url(r'^signout/$', views.signout),
    url(r'^files/view/$', views.view_files),
    url(r'^files/upload/$', views.upload_file),
    url(r'^files/(\d+)/delete/$', views.delete_file),
    url(r'^files/(\d+)/status/$', views.edit_file),
]
