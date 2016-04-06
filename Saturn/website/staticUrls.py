from django.conf.urls import url
from website import views

urlpatterns = [
        url(r'^createSite/$',views.createSite),
        url(r'^selectTemplate/$',views.selectTemplate),
]
