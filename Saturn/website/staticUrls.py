from django.conf.urls import url
from website import views

urlpatterns = [
        url(r'^createSite/$',views.createSite),
        url(r'^selectTemplate/$',views.selectTemplate),
        url(r'^editPage/$',views.editPage),
        url(r'^editSite/$',views.editSite),
        url(r'^getSiteData/$',views.getSiteData),
]
